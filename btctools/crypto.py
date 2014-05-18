from __future__ import unicode_literals

import hashlib
import binascii


# Secp256k1 parameters
# See https://en.bitcoin.it/wiki/Secp256k1
P = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
A = 0
B = 7
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (GX, GY)

INF = (0, 0)


def hash160(data):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(data)

    return ripemd160.digest()


def sha256(data):
    """hashes a bytes array and return binary value."""
    digest = hashlib.sha256(data).digest()
    return digest


def double_sha256(data):
    """Double hash a bytes array and return a binary value."""
    hash = sha256(sha256(data))
    return hash


def sha256_hex(data):
    """Hashes a string and return a hex string."""
    data = sha256(data)
    hex = binascii.hexlify(data)
    return hex.decode('utf-8')


def double_sha256_hex(data):
    """Double hashes a string and return a hex string."""
    data = double_sha256(data)
    hex = binascii.hexlify(data)
    return hex.decode('utf-8')


def secp256k1_multiply(n):
    """Performs elliptic curve point multiplication to compute nG.

    See here:
        http://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication

    """
    return point_multiplication(n, G)


def is_infinite_point(p):
    return p == INF

def inv(a,n):
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        r = high/low
        nm, new = hm-lm*r, high-low*r
        lm, low, hm, high = nm, new, lm, low
    return lm % n


def point_multiplication(n, p):
    """Elliptic curve point multiplication.

    Let's use the double-and-add method, which is the simplest one.
    See here:
        http://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add

    """
    n %= P

    if n == 0:
        q = INF
    elif n % 2 == 1:
        q = point_addition(p, point_multiplication(n - 1, p))
    else:
        q = point_multiplication(n / 2, point_doubling(p))

    return q


def point_addition(p, q):
    """Elliptic curve point addition.

        http://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_addition

    """
    if is_infinite_point(p):
        return q

    if is_infinite_point(q):
        return p

    if p == q:
        return point_doubling(p)

    if p[0] == q[0]:
        return INF

    l = ((q[1] - p[1]) * inv(q[0] - p[0], P)) % P
    x = (l ** 2 - p[0] - q[0]) % P
    y = (l * (p[0] - x) - p[1]) % P
    return x, y


def point_doubling(p):
    """Elliptic curve point doubling.

        http://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_doubling

    """
    if is_infinite_point(p):
        return p

    l = ((3 * (p[0] ** 2) + A) * inv(2 * p[1], P)) % P
    x = (l ** 2 - 2 * p[0]) % P
    y = (l * (p[0] - x) - p[1]) % P

    return x, y
