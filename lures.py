from typing import List, Tuple
import os
class LureNotifier:
    TERMS = ['cisco', 'gmail', 'login', 'mail', 'paying', 'paypal', '.gov']

    def identify_lures(self, domains: List[str]) -> List[Tuple[str, List[str]]]:
        """
        Identifies potential phishing lures from a list of candidate domains

        :param domains: list of domains as strings
        :return: list of tuples (domain, [matched_terms...])
        """


    def notify(self, lures: List[Tuple[str, List[str]]]) -> List[Tuple[str, List[str]]]:
        """
        Notifies users if lures are found containing specific terms

        :param lures: output from self.identify_lures
        :return: list of tuples (domain, [user_ids...])
        """
        raise NotImplementedError()


def test_identify_lures():
    domains = ['paypal-login.appspot.com', 'ciscomail.com', 'cisco.heroku.com', 'apple.com']
    notifier = LureNotifier()
    # Expected: [(paypal-login.appspot.com, [paypal, login]), (ciscomail.com, [cisco, mail])]
    return notifier.identify_lures(domains)


def test_notify():
    lures = test_identify_lures()
    notifier = LureNotifier()
    # Expected: [(paypal-login.appspot.com, [B, E]), (ciscomail.com, [A, C, K, B, E])]
    return notifier.notify(lures)
