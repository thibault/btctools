# -*- coding: utf-8 -*-
"""

See here for more data about private keys:
    https://en.bitcoin.it/wiki/Private_key

"""
from __future__ import unicode_literals

import six
from os import urandom

from encoding import bytes_to_int, bytes_to_hex
from crypto import sha256


PRIVKEY_LENGTH = 256 / 8  # 256 bits / 32 bytes
PRIVKEY_MIN = 0x01
PRIVKEY_MAX = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


class KeyError(ValueError):
    pass


class PrivateKey(object):
    def __init__(self, bits):
        """Initialize the private key from a bytes array."""

        if not isinstance(bits, six.binary_type):
            raise KeyError('You must provide the key as a binary value')

        if len(bits) != PRIVKEY_LENGTH:
            raise KeyError('Please provide a {} bytes long key'.format(PRIVKEY_LENGTH))

        bits_int = bytes_to_int(bits)
        if bits_int < PRIVKEY_MIN or bits_int > PRIVKEY_MAX:
            raise KeyError('Your private key value is outside bounds')

        self.bits = bits

    def __str__(self):
        return bytes_to_hex(self.bits)


def get_random_key():
    """Generates a random private key.

    You should only use this for testing purpose… unless you like to take
    risks.

    """
    key_int = PRIVKEY_MIN - 1
    while(key_int < PRIVKEY_MIN or key_int > PRIVKEY_MAX):
        seed = urandom(256)  # Let's trust the OS here
        key = sha256(seed)
        key_int = bytes_to_int(key)

    return PrivateKey(key)
