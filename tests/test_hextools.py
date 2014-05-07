import unittest

from hextools import little_endian_varint


class TransactionTests(unittest.TestCase):

    def test_little_endian_varint(self):
        self.assertEqual(little_endian_varint(1), '01')
        self.assertEqual(little_endian_varint(16), '10')
        self.assertEqual(little_endian_varint(252), 'fc')
        self.assertEqual(little_endian_varint(253), 'fdfd00')
        self.assertEqual(little_endian_varint(254), 'fdfe00')
        self.assertEqual(little_endian_varint(255), 'fdff00')
        self.assertEqual(little_endian_varint(256), 'fd0001')
        self.assertEqual(little_endian_varint(65535), 'fdffff')
        self.assertEqual(little_endian_varint(65536), 'fe00000100')
        self.assertEqual(little_endian_varint(100000), 'fea0860100')
        self.assertEqual(little_endian_varint(4294967295), 'feffffffff')
        self.assertEqual(little_endian_varint(4294967296), 'ff0000000001000000')
        self.assertEqual(little_endian_varint(5000000000), 'ff00f2052a01000000')
