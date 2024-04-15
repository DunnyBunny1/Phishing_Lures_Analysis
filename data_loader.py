import os
import json
from typing import List


def load_graph_data() -> dict[str, set[str]]:
    """
    Represent the graph as an adjacency set - O(1) average case lookups for
    keys and value
    """
    file_path = os.path.join(os.getcwd(), 'graph.jsonlines')
    supervisors_to_members: dict[str, set[str]] = {}

    with open(file_path, 'rt') as f:  # Open the file in read - text mode
        # Each line contains a JSON dictionary - read thru each line
        for line in f:
            if not line:  # If the line is empty, simply continue
                continue
            # Try to load each line's JSON string into a Python dict
            # Each line represents a mapping of member id : member lead pairs
            try:
                relationship: dict[str, str] = json.loads(line)
            # If we are unable to parse JSON of the line, move on to next line
            except json.decoder.JSONDecodeError:
                continue
            member_id = relationship['id']
            supervisor = relationship['reports_to']
            # If the given member id has a supervisor...
            # Add the team member to the supervisor's set of overseen members
            if supervisor is not None:
                member_list = supervisors_to_members.setdefault(
                    supervisor, set()
                )
                member_list.add(member_id)
                supervisors_to_members[supervisor] = member_list

    return supervisors_to_members


def load_domains():
    # Read in our domains file - each domain is separated by a \n
    file_name: str = 'domains.txt'
    directory: str = os.getcwd()
    file_path: str = os.path.join(directory, file_name)

    domains: List[str] = []
    with open(file_path, 'rt') as f:  # Open the file in read - text mode
        # Read the file line by line, removing any leading or trailing spaces
        for line in f:
            domains.append(line.strip())
    return domains


def load_subscriptions_data() -> dict[str, set[str]]:
    subscriptions_file_path = os.path.join(
        os.getcwd(), 'subscriptions.jsonlines'
    )
    # Maps each phishing term to the team members that subscribe to that term
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
