from lures import LureNotifier
import os
from typing import List


def load_domains():
    # Read in our domains file - each domain is separated by a \n
    file_name: str = 'domains.txt'
    directory: str = os.getcwd()
    file_path: str = os.path.join(directory, file_name)

    domains: List[str] = []
    with open(file_path, 'rt') as f:  # Open the file in read - text mode
        # Read the file line by line,
        for line in f:
            domains.append(line.strip())
    return domains


def main():
    domains = load_domains()
    notifier = LureNotifier()
    potential_lures = notifier.identify_lures(domains)
    print(potential_lures)


if __name__ == '__main__':
    main()
