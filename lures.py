from typing import List, Tuple, FrozenSet
from data_loader import load_graph_data, load_subscriptions_data


class LureNotifier:
    """
    Utility class that provides methods to...
    - Identify potential phishing lures in a list of newly created domain names
    - Notify team members who are subscribed to the target terms associated with
     those lures.
    """

    # A list of target terms comonly associated with phishing lures
    TARGET_TERMS: List[str] = [
        'cisco', 'gmail', 'login', 'mail', 'paying', 'paypal', '.gov'
    ]

    @staticmethod
    def identify_lures(domains: List[str]) -> set[Tuple[str, frozenset[str]]]:
        """
        Identifies potential phishing lures from a list of candidate domains.
        A domain d qualifies as a potential lure if and only if d contains at
        least two target terms. Returns potential lures as a set of (domain :
        matched target term set) pairs.
        :param domains: List of domain names as strings
        :return: a set of 2-tuples of (domain, {matched_terms...}) pairs
        """
        potential_lures: dict[str, frozenset[str]] = {}
        # Iterate thru each domain name, adding any ID'd target terms to a set
        for domain in domains:
            matched_terms: set[str] = set()
            for target_term in LureNotifier.TARGET_TERMS:
                if target_term in domain:
                    matched_terms.add(target_term)
            # If we have at least 2 target terms in the domain, flag it
            # as a potential lure
            if len(matched_terms) >= 2:
                potential_lures[domain] = frozenset(matched_terms)

        # Return a set of 2-tuples: (domain name, matched terms set) pairs
        return {
            (domain, matches) for domain, matches in potential_lures.items()
        }

    @staticmethod
    def notify(lures: set[Tuple[str, frozenset[str]]]) -> set[Tuple[str,
    frozenset[str]]]:
        """
        Given a set of potential phishing lures (domain : matched target term
        set) pairs, alerts any team member that is subscribed to the target
        term of the phishing lure domain name.
        In order to "alert" a team, the given team and all of the team's
        subteams must also be alerted.
        A team is s is a subteam given team t if s is directly supervised by t
        or s is in indirectly supervised by t (ex. s is a subteam of team k,
        and k is a subteam of t or k is a subteam of some subteam of ... t)
        :param lures: the set of phisihing lures (domain :matched target term
        set) pairs
        :return a set of notification alerts, representted as a set of (domain :
        alerted team id string) pairs
        """
        supervisors_to_members: dict[str, set[str]] = load_graph_data()
        term_to_members: dict[str, set[str]] = load_subscriptions_data()

        domains_to_alerted_teams: dict[str, FrozenSet[str]] = {}
        # For each phishing lure term in each domain, alert each team member
        # and their respective subteams
        for domain, matched_terms in lures:
            domains_to_alerted_teams[domain] = bfs(
                matched_terms, term_to_members, supervisors_to_members
            )
        return {
            (domain, alerted_teams) for domain, alerted_teams in
            domains_to_alerted_teams.items()
        }


def bfs(matched_terms, term_to_members, supervisors_to_members):
    """
    Performs a breadth-first search to alert team members of newly registered
    domain names that may contain phishing lures to target terms for which
    team members are subscribed. For each target term found in a potential
    lure, notifies each team member that is directly subscribed to the target
    term as well as any descendants (subteams) of the notified teams.
    :param matched_terms: a set of target terms found in a single domain name,
    each target term will have alerts raised for it
    :param term_to_members: a mapping of each term to the set of team members
    that subscribe to alerts for that term
    :param supervisors_to_members: a mapping of supervisor IDs to their set of
    direct team members' IDs
    :return: a set of all the team members IDs (a set of strings) that should be
    alerted for the given matched terms.
    """
    # Keep track of the members we must notify for the given term
    members_to_be_notified = set()
    # For each phishing term in the domain, notify each team member
    # and each subteam
    for term in matched_terms:
        frontier = []
        # Add of the immediate notifications for the given term
        frontier.extend(term_to_members[term])
        while frontier:  # While we have unnotified team members:
            # Add the current member to the set of
            curr_member = frontier.pop(0)
            members_to_be_notified.add(curr_member)
            # Add each team members subteams to the queue if the team
            # member has any subteams
            if curr_member in supervisors_to_members:
                frontier.extend(supervisors_to_members[curr_member])
    return frozenset(members_to_be_notified)
