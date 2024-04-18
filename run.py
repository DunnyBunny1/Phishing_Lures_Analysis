# Std lib modules
from typing import List, Tuple
# Custom modules
from lures import LureNotifier
from data_loader import load_domains


def main():
    domains: List[str] = load_domains()
    potential_lures: set[Tuple[str, frozenset[str]]] = \
        LureNotifier.identify_lures(domains)
    for domain, matched_terms in potential_lures:
        print(f'Domain: {domain} Matched terms: {matched_terms}\n')


if __name__ == '__main__':
    main()
