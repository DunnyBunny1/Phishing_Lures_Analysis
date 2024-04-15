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
        expected_lures: Set[Tuple[str, frozenset[str]]] = {
            ('paypal-login.appspot.com', frozenset(['paypal', 'login'])),
            ('ciscomail.com', frozenset(['cisco', 'mail']))
        }
        actual_lures = LureNotifier.identify_lures(domains)
        self.assertEqual(expected_lures, actual_lures)

        expected_notifications = {
            ('paypal-login.appspot.com', frozenset(['B', 'E'])),
            ('ciscomail.com', frozenset(['A', 'C', 'K', 'B', 'E']))
        }
        actual_notifications = LureNotifier.notify(actual_lures)
        self.assertEqual(expected_notifications, actual_notifications)

    def test_notify_for_multiple_domains(self):
        domains = [
            'login.cisco.paying.gmail.com'
        ]
        expected_lures: Set[Tuple[str, frozenset[str]]] = {
            ('login.cisco.paying.gmail.com', frozenset(['login', 'paying',
                                                        'cisco', 'gmail'])),
        }
        actual_lures = LureNotifier.identify_lures(domains)
        self.assertEqual(expected_lures, actual_lures)

        expected_notifications = {
            ('paypal-login.appspot.com', frozenset(['B', 'E'])),
            ('ciscomail.com', frozenset(['A', 'C', 'K', 'B', 'E']))
        }
        actual_notifications = LureNotifier.notify(actual_lures)
        self.assertEqual(expected_notifications, actual_notifications)
