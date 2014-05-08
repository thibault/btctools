from __future__ import unicode_literals

import unittest

from addresses.b58 import b58_encode, b58_decode


class B58Tests(unittest.TestCase):

    def test_b58_encode(self):
        self.assertEqual(b58_encode('toto'), '3yd11G')
        self.assertEqual(b58_encode('schtroumpf'), '7UztRfowQ4Rhc9')
        self.assertEqual(b58_encode('gloubiboulga'), '2xCVX7gSj2Xfeinet')

    def test_b58_decode(self):
        self.assertEqual('toto', b58_decode('3yd11G'))
        self.assertEqual('schtroumpf', b58_decode('7UztRfowQ4Rhc9'))
        self.assertEqual('gloubiboulga', b58_decode('2xCVX7gSj2Xfeinet'))
