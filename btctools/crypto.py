from __future__ import unicode_literals

import hashlib
import binascii

from ripemd import RIPEMD160


def hash160(string):
    data = string.encode('utf-8')
    return RIPEMD160(data).digest()


def _sha256_bin(data):
    """hashes a bytes array and return binary value."""
    digest = hashlib.sha256(data).digest()
    return digest


def sha256(string):
    """Hashes a string and return a bytes array."""
    data = string.encode('utf-8')
    hash = _sha256_bin(data)
    return hash


def double_sha256(string):
    """Double hash a string and return a bytes array."""
    data = string.encode('utf-8')
    hash = _sha256_bin(_sha256_bin(data))
    return hash


def sha256_hex(string):
    """Hashes a string and return a hex string."""
    data = sha256(string)
    hex = binascii.hexlify(data)
    return hex.decode('utf-8')


def double_sha256_hex(string):
    """Double hashes a string and return a hex string."""
    data = double_sha256(string)
    hex = binascii.hexlify(data)
    return hex.decode('utf-8')


def bytes_to_int(bytes):
    """Converts a bytes array into a big number."""
    hex_data = binascii.hexlify(bytes).encode('utf-8')
    number = int(hex_data, 16)

    return number
