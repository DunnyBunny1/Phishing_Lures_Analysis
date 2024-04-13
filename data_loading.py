import os
import json
from typing import List


def load_graph_data():
    file_path = os.path.join(os.getcwd(), 'graph.jsonlines')
    supervisors_to_members: dict[str, List[str]] = {}

    with open(file_path, 'rt') as f:  # Open the file in read - text mode
        # Read the file line by line, removing any leading / trailing spaces
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
            if supervisor:
                member_list = supervisors_to_members.setdefault(supervisor, [])
                member_list.append(member_id)
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


def load_subscriptions_data():
    subscriptions_file_path = os.path.join(
        os.getcwd(), 'subscriptions.jsonlines'
    )
    # TODO: Implement
