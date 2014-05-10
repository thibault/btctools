from __future__ import unicode_literals

import unittest

from encoding import b58_encode, b58_decode, b58c_encode, b58c_decode


class EncodingTests(unittest.TestCase):

    def test_b58_encode(self):
        self.assertEqual(b58_encode(b'toto'), b'3yd11G')
        self.assertEqual(b58_encode(b'schtroumpf'), b'7UztRfowQ4Rhc9')
        self.assertEqual(b58_encode(b'gloubiboulga'), b'2xCVX7gSj2Xfeinet')

    def test_b58_decode(self):
        self.assertEqual(b'toto', b58_decode(b'3yd11G'))
        self.assertEqual(b'schtroumpf', b58_decode(b'7UztRfowQ4Rhc9'))
        self.assertEqual(b'gloubiboulga', b58_decode(b'2xCVX7gSj2Xfeinet'))

    def test_b58c_encode(self):
        self.assertEqual(b58c_encode(b'toto'), b'1LUZzwD2kVJP')
        self.assertEqual(b58c_encode(b'schtroumpf'), b'1jRQ85MdGSpWi8xkom5e')
        self.assertEqual(b58c_encode(b'gloubiboulga'), b'1DmjGGCeE3oJPafCwfhNZGz')

    def test_b58c_decode(self):
        self.assertEqual(b'toto', b58c_decode(b'1LUZzwD2kVJP'))
        self.assertEqual(b'schtroumpf', b58c_decode(b'1jRQ85MdGSpWi8xkom5e'))
        self.assertEqual(b'gloubiboulga', b58c_decode(b'1DmjGGCeE3oJPafCwfhNZGz'))
