# -*- coding: utf-8 -*-
"""

See here for more data about private keys:
    https://en.bitcoin.it/wiki/Private_key

"""
from __future__ import unicode_literals

import six
from os import urandom

from encoding import (
    bytes_to_int, int_to_bytes, bytes_to_hex, hex_to_bytes, b58c_encode)
from crypto import sha256, hash160
from curves import secp256k1_multiply


PRIVKEY_LENGTH = 256 / 8  # 256 bits / 32 bytes
PRIVKEY_MIN = 0x01
PRIVKEY_MAX = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


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

    def as_hex(self):
        return bytes_to_hex(self.bits)

    def as_wif(self):
        """Wallet Import Format generation.

        See here:
            https://en.bitcoin.it/wiki/Wallet_import_format

        """
        b58 = b58c_encode(self.bits, b'\x80')
        return b58

    def as_int(self):
        return bytes_to_int(self.bits)

    # TODO memoize
    def get_public_key(self):
        """Get the associated public key."""
        n = bytes_to_int(self.bits)
        nG = secp256k1_multiply(n)

        pubkey = b''.join([
            b'\x04',
            int_to_bytes(nG[0]).ljust(32, b'\x00'),
            int_to_bytes(nG[1]).ljust(32, b'\x00')
        ])

        return pubkey

    def get_address(self):
        """Get the associated Bitcoin address."""
        pubkey = self.get_public_key()
        hash = hash160(sha256(pubkey))
        return b58c_encode(hash)


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


def get_key_from_hex(hexa):
    """Creates a private key from an hexa string."""
    bits = hex_to_bytes(hexa)
    return PrivateKey(bits)
