# Std lib modules
from typing import List, Tuple
# Custom modules
from lures import LureNotifier
from data_loader import load_graph_data, load_domains, load_subscriptions_data


def main():
    domains: List[str] = load_domains()
    potential_lures: set[Tuple[str, frozenset[str]]] = \
        LureNotifier.identify_lures(domains)
    print(load_subscriptions_data())
    print(load_graph_data())


if __name__ == '__main__':
    main()
