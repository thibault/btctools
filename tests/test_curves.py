from __future__ import unicode_literals

import unittest

from curves import EllipticCurve, Point, Inf, mod_inverse


class CurveTests(unittest.TestCase):

    def test_mod_inverse(self):
        self.assertEqual(mod_inverse(3, 11), 4)
        self.assertEqual(mod_inverse(42, 2017), 1969)

    def test_has_point(self):
        curve = EllipticCurve(-2, 4, 17)
        with self.assertRaises(ValueError):
            Point(curve, 3, 6)

    def test_addition(self):
        curve = EllipticCurve(-2, 4, 17)
        P = Point(curve, 3, 5)
        Q = Point(curve, 0, 2)
        Z = Inf(curve)

        self.assertEqual(P + Q, Point(curve, 15, 0))
        self.assertEqual(P + Q, Q + P)
        self.assertEqual(P + Z, P)
        self.assertEqual(Z + Z, Z)

    def test_multiplication(self):
        curve = EllipticCurve(-2, 4, 17)
        P = Point(curve, 3, 5)

        self.assertEqual(2 * P, P + P)
        self.assertEqual(3 * P, P + P + P)
        self.assertEqual(5 * P, P + P + P + P + P)
