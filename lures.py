from typing import List, Tuple, Dict
import os


class LureNotifier:
    TERMS = ['cisco', 'gmail', 'login', 'mail', 'paying', 'paypal', '.gov']

    def identify_lures(self, domains: List[str]) -> List[Tuple[str, List[str]]]:
        """
        Identifies potential phishing lures from a list of candidate domains.
        A domain qualifies as a potential lure if and only if it contains at
        least two target terms.
        :param domains: list of domains as strings
        :return: list of tuples (domain, [matched_terms...])
        """
        target_terms: List[str] = [
            'cisco', 'gmail', 'login', 'mail', 'paying', 'paypal', '.gov'
        ]

        potential_lures: dict[str, List[str]] = {}
        # Iterate thru each domain name, adding any ID'd target terms to a list
        for domain in domains:
            matched_terms: List[str] = []
            for target_term in target_terms:
                if target_term in domain:
                    matched_terms.append(target_term)
            # If we have at least 2 target terms in the domain, identify it
            # as a potential lure
            if len(matched_terms) >= 2:
                potential_lures[domain] = matched_terms

        # Return a list of 2-tuples: (domain name, matched terms list) pairs
        return [
            (domain, matches) for domain, matches in potential_lures.items()
        ]

    def notify(self, lures: List[Tuple[str, List[str]]]) -> List[
        Tuple[str, List[str]]]:
        """
        Notifies users if lures are found containing specific terms

        :param lures: output from self.identify_lures
        :return: list of tuples (domain, [user_ids...])
        """
        raise NotImplementedError()


def test_identify_lures():
    domains = ['paypal-login.appspot.com', 'ciscomail.com', 'cisco.heroku.com',
               'apple.com']
    notifier = LureNotifier()
    # Expected: [(paypal-login.appspot.com, [paypal, login]), (ciscomail.com, [cisco, mail])]
    return notifier.identify_lures(domains)


def test_notify():
    lures = test_identify_lures()
    notifier = LureNotifier()
    # Expected: [(paypal-login.appspot.com, [B, E]), (ciscomail.com, [A, C, K, B, E])]
    return notifier.notify(lures)
