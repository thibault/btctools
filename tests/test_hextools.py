import unittest

from hextools import var_length_int


class TransactionTests(unittest.TestCase):

    def test_var_length_int(self):
        self.assertEqual(var_length_int(1), '01')
        self.assertEqual(var_length_int(16), '10')
        self.assertEqual(var_length_int(252), 'fc')
        self.assertEqual(var_length_int(253), 'fdfd00')
        self.assertEqual(var_length_int(254), 'fdfe00')
        self.assertEqual(var_length_int(255), 'fdff00')
        self.assertEqual(var_length_int(256), 'fd0001')
        self.assertEqual(var_length_int(65535), 'fdffff')
        self.assertEqual(var_length_int(65536), 'fe00000100')
        self.assertEqual(var_length_int(100000), 'fea0860100')
        self.assertEqual(var_length_int(4294967295), 'feffffffff')
        self.assertEqual(var_length_int(4294967296), 'ff0000000001000000')
        self.assertEqual(var_length_int(5000000000), 'ff00f2052a01000000')
