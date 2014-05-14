from __future__ import unicode_literals

import unittest

from keys import KeyError, PrivateKey, get_random_key


class PrivateKeyTests(unittest.TestCase):

    def test_key_initialization(self):

        with self.assertRaises(KeyError):
            PrivateKey('toto')

        with self.assertRaises(KeyError):
            PrivateKey(b'\x01')

        with self.assertRaises(KeyError):
            PrivateKey(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

        with self.assertRaises(KeyError):
            PrivateKey(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE\xBA\xAE\xDC\xE6\xAF\x48\xA0\x3B\xBF\xD2\x5E\x8C\xD0\x36\x41\x42')

        PrivateKey(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE\xBA\xAE\xDC\xE6\xAF\x48\xA0\x3B\xBF\xD2\x5E\x8C\xD0\x36\x41\x41')
        self.assertTrue(True)

    def test_get_random_key(self):
        key = get_random_key()
        self.assertTrue(isinstance(key, PrivateKey))