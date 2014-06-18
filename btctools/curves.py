from __future__ import unicode_literals

from random import randint
from encoding import bytes_to_int


# Secp256k1 parameters
# See https://en.bitcoin.it/wiki/Secp256k1
P = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
A = 0
B = 7
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (GX, GY)
INF = (0, 0)


def mod_inverse(a, n):
    """Return the inverse of a mod b

    >>> mod_inverse(42, 2017)
    1969

    """
    b = n
    if abs(b) == 0:
        return (1, 0, a)

    x1, x2, y1, y2 = 0, 1, 1, 0
    while abs(b) > 0:
        q, r = divmod(a, b)
        x = x2 - q * x1
        y = y2 - q * y1
        a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y

    return x2 % n


class EllipticCurve(object):
    """Represents a single elliptic curve defined over a finite field.

    See here:
        http://en.wikipedia.org/wiki/Elliptic_curve
        http://jeremykun.com/2014/02/24/elliptic-curves-as-python-objects/


    p must be prime, since we use the modular inverse to compute point
    addition.

    """
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def __eq__(self, C):
        return (self.a, self.b) == (C.a, C.b)

    def has_point(self, x, y):
        return (y ** 2) % self.p == (x ** 3 + self.a * x + self.b) % self.p

    def __str__(self):
        return 'y^2 = x^3 + {}x + {}'.format(self.a, self.b)


class Point(object):
    """A point on a specific curve."""
    def __init__(self, curve, x, y):
        self.curve = curve
        self.x = x % curve.p
        self.y = y % curve.p

        if not self.curve.has_point(x, y):
            raise ValueError('{} is not on curve {}'.format(self, self.curve))

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __getitem__(self, index):
        return [self.x, self.y][index]

    def __eq__(self, Q):
        return (self.curve, self.x, self.y) == (Q.curve, Q.x, Q.y)

    def __neg__(self):
        return Point(self.curve, self.x, -self.y)

    def __add__(self, Q):
        """Add two points together.

        We need to take care of special cases:
         * Q is the infinity point (0)
         * P == Q
         * The line crossing P and Q is vertical.

        """
        assert self.curve == Q.curve

        # 0 + P = P
        if isinstance(Q, Inf):
            return self

        xp, yp, xq, yq = self.x, self.y, Q.x, Q.y
        m = None

        # P == Q
        if self == Q:
            if self.y == 0:
                R = Inf(self.curve)
            else:
                m = ((3 * xp * xp + self.curve.a) * mod_inverse(2 * yp, self.curve.p)) % self.curve.p

        # Vertical line
        elif xp == xq:
            R = Inf(self.curve)

        # Common case
        else:
            m = ((yq - yp) * mod_inverse(xq - xp, self.curve.p)) % self.curve.p

        if m is not None:
            xr = (m ** 2 - xp - xq) % self.curve.p
            yr = (m * (xp - xr) - yp) % self.curve.p
            R = Point(self.curve, xr, yr)

        return R

    def __mul__(self, n):
        assert isinstance(n, (int, long))
        assert n > 0

        n = n % self.curve.p

        if n == 0:
            return Inf(self.curve)

        else:
            Q = self
            R = self if n & 1 == 1 else Inf(self.curve)

            i = 2
            while i <= n:
                Q = Q + Q

                if n & i == i:
                    R = Q + R

                i = i << 1

        return R

    def __rmul__(self, n):
        return self * n


class Inf(Point):
    """The custom infinity point."""
    def __init__(self, curve):
        self.curve = curve

    def __str__(self):
        return 'Inf'

    def __eq__(self, Q):
        return isinstance(Q, Inf)

    def __neg__(self):
        """-0 = 0"""
        return self

    def __add__(self, Q):
        """P + 0 = 0"""
        return Q

    def __mul__(self, n):
        assert isinstance(n, (int, long))
        return self


class ECDSA(object):
    def __init__(self, curve, generator):
        self.curve = curve
        self.G = generator

    def generate_k(self):
        # TODO deterministic generate k
        k = randint(1, self.curve.p - 1)
        return k

    def sign(self, message, privkey):
        N = self.curve.p
        msg = bytes_to_int(message)
        k = self.generate_k()
        r, j = k * self.G
        s = (mod_inverse(k, N) * (msg + r * privkey.as_int())) % N
        return r, s


secp256k1 = EllipticCurve(A, B, P)
G = Point(secp256k1, GX, GY)
secp256k1_ecdsa = ECDSA(secp256k1, G)


def secp256k1_multiply(n):
    """Performs elliptic curve point multiplication to compute n * G.

    See here:
        http://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication

    """
    return n * G


def secp256k1_sign(message, privkey):
    """Sign message using Elliptic Curve DSA.

    See here:
        http://en.wikipedia.org/wiki/Elliptic_Curve_DSA

    """
    return secp256k1_ecdsa.sign(message, privkey)
