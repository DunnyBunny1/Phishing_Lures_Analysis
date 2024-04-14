import unittest
from lures import LureNotifier
from typing import List, Tuple, Set


class TestLureNotifier(unittest.TestCase):

    def test_identify_lures(self):
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

    def test_notify(self):
        domains = [
            'paypal-login.appspot.com', 'ciscomail.com',
            'cisco.heroku.com', 'apple.com'
        ]
        lures = LureNotifier.identify_lures(domains)
        expected_notifications = {
            ('paypal-login.appspot.com', frozenset(['B', 'E'])),
            ('ciscomail.com', frozenset(['A', 'C', 'K', 'B', 'E']))
        }
        actual_notifications = LureNotifier.notify(lures)
        self.assertEqual(expected_notifications, actual_notifications)


