from __future__ import unicode_literals

import unittest

from addresses.b58 import b58_encode, b58_decode, b58c_encode, b58c_decode


class B58Tests(unittest.TestCase):

    def test_b58_encode(self):
        self.assertEqual(b58_encode('toto'), '3yd11G')
        self.assertEqual(b58_encode('schtroumpf'), '7UztRfowQ4Rhc9')
        self.assertEqual(b58_encode('gloubiboulga'), '2xCVX7gSj2Xfeinet')

    def test_b58_decode(self):
        self.assertEqual('toto', b58_decode('3yd11G'))
        self.assertEqual('schtroumpf', b58_decode('7UztRfowQ4Rhc9'))
        self.assertEqual('gloubiboulga', b58_decode('2xCVX7gSj2Xfeinet'))

    def test_b58c_encode(self):
        self.assertEqual(b58c_encode('toto'), '1LUZzwD2kVJP')
        self.assertEqual(b58c_encode('schtroumpf'), '1jRQ85MdGSpWi8xkom5e')
        self.assertEqual(b58c_encode('gloubiboulga'), '1DmjGGCeE3oJPafCwfhNZGz')

    def test_b58c_decode(self):
        self.assertEqual('toto', b58c_decode('1LUZzwD2kVJP'))
        self.assertEqual('schtroumpf', b58c_decode('1jRQ85MdGSpWi8xkom5e'))
        self.assertEqual('gloubiboulga', b58c_decode('1DmjGGCeE3oJPafCwfhNZGz'))
