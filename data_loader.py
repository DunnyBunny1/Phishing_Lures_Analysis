import os
import json
from typing import List


def load_graph_data() -> dict[str, set[str]]:
    """
    Reads in graph JSON data and returns an adjacency set dictionary mapping
    each supervisor to its set of team members.
    Represents the graph as an adjacency set - O(1) average case lookups for
    keys and value.
    :raises ValueError if we are unable to properly read in the graph data to
    populate the adjacency set
    :raises FileNotFound error if the configuration file does not exist
    :return a mapping of supervisor IDs to their set of direct team members' IDs
    """
    file_path: str = os.path.join(os.getcwd(), 'data', 'graph.jsonlines')
    # Mapping of supervisors to its set of team members
    supervisors_to_members: dict[str, set[str]] = {}

    with open(file_path, 'rt') as f:  # Open the file in read - text mode
        # Read thru each line (each line contains a JSON dictionary)
        for line in f:
            if not line:  # If the line is empty, simply continue
                continue
            # Try to load each line's JSON string into a Python dict
            # Each line represents a mapping of member id : member lead pairs
            try:
                relationship: dict[str, str] = json.loads(line)
            # If we are unable to parse JSON of the line, move on to next line
            # TODO: Consider handling the error in another way (ex.
            #  propagating it up)
            except json.decoder.JSONDecodeError:
                continue
            member_id: str = relationship['id']
            supervisor: str = relationship['reports_to']
            # If the given member id has a supervisor...
            # Add the team member to the supervisor's set of overseen members
            if supervisor is not None:
                member_list = supervisors_to_members.setdefault(
                    supervisor, set()
                )
                member_list.add(member_id)
                supervisors_to_members[supervisor] = member_list
    if not supervisors_to_members:
        raise ValueError('Supervisors to team members incorrectly populated '
                         'with graph data')
    return supervisors_to_members


def load_domains() -> List[str]:
    """
    Reads in a set of newly registered domain names and returns them as a
    list of strings
    :return the List of domain name strings
    :raises FileNotFound error if the configuration file does not exist
    """
    # Read in our domains file - each domain is separated by a \n
    file_name: str = 'domains.txt'
    file_path: str = os.path.join(os.getcwd(), 'data', file_name)

    domains: List[str] = []
    with open(file_path, 'rt') as f:  # Open the file in read - text mode
        # Read the file line by line, removing any leading or trailing spaces
        for line in f:
            domains.append(line.strip())
    return domains


def load_subscriptions_data() -> dict[str, set[str]]:
    """
    Reads in subscription JSON data, where a subscription represents a target
    term for which a team member should be alerted if a domain name containing
    the target term is registered.
    :return: a mapping of target terms (strings) to a set of team member IDs
    (strings) for team members are directly subscribed to that term.
    :raises FileNotFound error if the configuration file does not exist
    """
    subscriptions_file_path = os.path.join(
        os.getcwd(), 'data', 'subscriptions.jsonlines'
    )
    # Maps each term to the set of team members that subscribe to that term
    term_to_members: dict[str, set[str]] = {}
    # Open the subscriptions file in read-text mode
    with open(subscriptions_file_path, 'rt') as f:
        # Try to read each line of the file as a JSON dictionary
        for line in f:
            if not line:  # If the line is empty, simply continue
                continue
            # Try to load each line's JSON string into a Python dict
            # Each line is a mapping of subscribed term  : member id pairs
            try:
                subscription: dict[str, str] = json.loads(line)
            # If we are unable to parse JSON of the line, move on to next line
            except json.decoder.JSONDecodeError:
                continue
            # Add the term to the member's mapping of subscribed terms
            member = subscription['id']
            term = subscription['term']
            # If a term does not have a set of mapped members, create a new one
            member_set = term_to_members.setdefault(term, set())
            member_set.add(member)  # Add the member to term's set of members
            term_to_members[term] = member_set
    return term_to_members
