import unittest
from lures import LureNotifier
from typing import Tuple, Set


class TestLureNotifier(unittest.TestCase):
    """
    Unit tests for the LureNotifier class
    """

    def test_identify_lures_with_multiple_matches(self):
        """
        Tests lure identification for domains containing multiple target
        terms. Creates domain names each containing at least 2 matching
        target terms, and asserts that each target term is correctly extracted
        from each domain
        """
        domains = [
            'paypal-login.appspot.com', 'ciscomail.com',
            'cisco.heroku.com', 'apple.com'
        ]
        expected_lures: Set[Tuple[str, frozenset[str]]] = {
            ('paypal-login.appspot.com', frozenset(['paypal', 'login'])),
            ('ciscomail.com', frozenset(['cisco', 'mail']))
        }
        actual_lures = LureNotifier.identify_lures(domains)
        self.assertEqual(expected_lures, actual_lures)

    def test_identify_lures_ignores_only_one_match(self):
        """
        Tests that lures are not identified in domains with less than 2
        matching terms. Creates domains each only containing exactly 1 matching
        target term, so the given set of domains should not trigger
        any identified lures.
        """
        domains = [
            'paypal_fake.com', 'mail.apple.com',
            'usa.login.com', 'accounts.paying.com'
        ]
        # Since each domain only has one target term, none of them should get
        # flagged as potential phishing lures
        expected_lures = set()
        actual_lures = LureNotifier.identify_lures(domains)
        self.assertEqual(expected_lures, actual_lures)

    def test_notify_with_multiple_domains(self):
        """
        Tests that the notify() method correctly traverses the supervisor to
        manager graph. The detected term "mail" should notify both nodes K and C
        (sibling nodes), but not the parent node A (since only K and C have
        "mail" notifications configured. In addition, all of C's descendants
        (B,and E)
        """
        lures: Set[Tuple[str, frozenset[str]]] = {
            ('fake_mail_website.com', frozenset(['mail'])),
        }

        expected_notifications = {
            ('fake_mail_website.com', frozenset(['K', 'C', 'B', 'E'])),
        }
        actual_notifications = LureNotifier.notify(lures)
        self.assertEqual(expected_notifications, actual_notifications)
        # Ensure that the parent node of K and C does not get notified as well
        self.assertTrue('A' not in actual_notifications)

    def test_notify_alerts_all_nodes_from_root(self):
        """
        Tests that all nodes (team members) are notified when a phishing lure
        containing a term t is detected, and the root supervisor is subscribed
        to alerts for the term t.
        """
        domains = [
            'fakesite_login.gov',
        ]
        expected_lures: Set[Tuple[str, frozenset[str]]] = {
            ('fakesite_login.gov', frozenset(['.gov', 'login']))
        }
        actual_lures = LureNotifier.identify_lures(domains)
        self.assertEqual(expected_lures, actual_lures)
        # Since A is the root supervisor and subscribed to .gov, all nodes
        # should be notified
        gov_notifications = {'A', 'C', 'K', 'B', 'E'}
        expected_notifications = {
            ('fakesite_login.gov', frozenset(gov_notifications))
        }
        actual_notifications = LureNotifier.notify(actual_lures)
        self.assertEqual(expected_notifications, actual_notifications)

    def test_notify_from_leaf_node(self):
        """
        Ensures that only the lowest level team member (a leaf node in the
        supervisor tree) gets notified when a phishing lure for which they
        are the only node subscribed gets detected.
        """
        domains = [
            'paying.paypal.com',
        ]
        expected_lures: Set[Tuple[str, frozenset[str]]] = {
            ('paying.paypal.com', frozenset(['paying', 'paypal']))
        }
        actual_lures = LureNotifier.identify_lures(domains)
        self.assertEqual(expected_lures, actual_lures)
        # Since E is a leaf node and the only node subscribed to paying and
        # PayPal, E should be the only  team notified
        expected_notifications = {
            ('paying.paypal.com', frozenset('E'))
        }
        actual_notifications = LureNotifier.notify(actual_lures)
        self.assertEqual(expected_notifications, actual_notifications)
