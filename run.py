# Std lib modules
from typing import List, Tuple
# Custom modules
from lures import LureNotifier
from data_loader import load_graph_data, load_domains, load_subscriptions_data


def main():
    domains: List[str] = load_domains()
    supervisors_to_members: dict[str, set[str]] = load_graph_data()
    member_to_terms : dict[str, set[str]] = load_subscriptions_data()
    potential_lures: List[Tuple[str, List[str]]] = \
        LureNotifier.identify_lures(domains)


if __name__ == '__main__':
    main()
