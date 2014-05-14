from __future__ import unicode_literals

import unittest

from keys import KeyError, PrivateKey, get_random_key


class PrivateKeyTests(unittest.TestCase):

    def setUp(self):
        bits = b"\x0c(\xfc\xa3\x86\xc7\xa2'`\x0b/\xe5\x0b|\xae\x11\xec\x86\xd3\xbf\x1f\xbeG\x1b\xe8\x98'\xe1\x9dr\xaa\x1d"
        self.key = PrivateKey(bits)

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

    def test_as_hex(self):
        self.assertEqual(
            self.key.as_hex(),
            '0c28fca386c7a227600b2fe50b7cae11ec86d3bf1fbe471be89827e19d72aa1d'
        )

    def test_as_wif(self):
        self.assertEqual(
            self.key.as_wif(),
            '5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ'
        )
