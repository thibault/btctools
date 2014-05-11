from __future__ import unicode_literals

import unittest

from encoding import (
    b58_encode, b58_decode, b58c_encode, b58c_decode, little_endian_varint
)


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


class EndiannesTests(unittest.TestCase):

    def test_little_endian_varint(self):
        self.assertEqual(little_endian_varint(1), b'\x01')
        self.assertEqual(little_endian_varint(16), b'\x10')
        self.assertEqual(little_endian_varint(252), b'\xfc')
        self.assertEqual(little_endian_varint(253), b'\xfd\xfd\x00')
        self.assertEqual(little_endian_varint(254), b'\xfd\xfe\x00')
        self.assertEqual(little_endian_varint(255), b'\xfd\xff\x00')
        self.assertEqual(little_endian_varint(256), b'\xfd\x00\x01')
        self.assertEqual(little_endian_varint(65535), b'\xfd\xff\xff')
        self.assertEqual(little_endian_varint(65536), b'\xfe\x00\x00\x01\x00')
        self.assertEqual(little_endian_varint(100000), b'\xfe\xa0\x86\x01\x00')
        self.assertEqual(little_endian_varint(4294967295), b'\xfe\xff\xff\xff\xff')
        self.assertEqual(little_endian_varint(4294967296), b'\xff\x00\x00\x00\x00\x01\x00\x00\x00')
        self.assertEqual(little_endian_varint(5000000000), b'\xff\x00\xf2\x05\x2a\x01\x00\x00\x00')
