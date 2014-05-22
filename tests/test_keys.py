from __future__ import unicode_literals

import unittest

from keys import KeyError, PrivateKey, get_random_key, get_key_from_hex


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

    def test_get_key_from_hex(self):
        hexa = '0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D'
        key = get_key_from_hex(hexa)
        self.assertEqual(
            key.as_hex(),
            '0c28fca386c7a227600b2fe50b7cae11ec86d3bf1fbe471be89827e19d72aa1d'
        )

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

    def test_get_public_key(self):
        pubkey = self.key.get_public_key()

        key = b'\x04\xd0\xde\x0a\xae\xae\xfa\xd0\x2b\x8b\xdc\x8a\x01\xa1\xb8\xb1\x1c\x69\x6b\xd3\xd6\x6a\x2c\x5f\x10\x78\x0d\x95\xb7\xdf\x42\x64\x5c\xd8\x52\x28\xa6\xfb\x29\x94\x0e\x85\x8e\x7e\x55\x84\x2a\xe2\xbd\x11\x5d\x1e\xd7\xcc\x0e\x82\xd9\x34\xe9\x29\xc9\x76\x48\xcb\x0a'
        self.assertEqual(
            pubkey,
            key
        )

    def test_get_address(self):
        address = self.key.get_address()
        self.assertEqual(
            '1GAehh7TsJAHuUAeKZcXf5CnwuGuGgyX2S',
            address
        )
