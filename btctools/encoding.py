"""Encoding tools.

The encoding module mostly works from and to bytes arrays.

"""
from __future__ import unicode_literals

import six
import binascii

from crypto import double_sha256


B58 = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
B256 = b''.join([six.int2byte(x) for x in range(256)])


def enforce_bytes(func):
    """Type checking decorator.

    Working on the correct data type is critical for encoding conversion
    methods. This decorator makes sure the decorated function first parameter
    is of the binary type (str or bytes, depending on Python version.

    """
    def _enforce_bytes(data, *args, **kwargs):
        if not isinstance(data, six.binary_type):
            raise ValueError('You need to pass binary data (str in Py2, bytes in Py3')
        return func(data, *args, **kwargs)
    return _enforce_bytes


@enforce_bytes
def bytes_to_int(bytes):
    """Converts a bytes array into a big number."""
    return base_to_int(bytes, B256)


@enforce_bytes
def bytes_to_hex(bytes):
    """Converts an array of bytes into a hex string.

    >>> address = '1EL3y9j8rzZwa8Hxmx2scatb3bh8KKFK6v'.encode('utf-8')
    >>> bytes_to_hex(address)
    '9234042049764dbed331c7d1fc492a4eb5007c53'

    """
    return binascii.hexlify(bytes).decode('ascii')


def hex_to_bytes(hex):
    return binascii.unhexlify(hex)


@enforce_bytes
def base_to_int(string, base_str):
    """Converts an array of bytes encoded in a given base into a binary number."""
    value = 0
    base = len(base_str)
    for b in string:
        value *= base
        value += base_str.find(b)

    return value


def int_to_base(number, base_str):
    """Converts a number into an array of bytes encoded in the given base."""
    value = []
    base = len(base_str)
    while number > 0:
        value = [base_str[number % base]] + value
        number -= number % base
        number //= base

    # Python 2 / 3 compatibility from hell
    return b''.join(map(six.int2byte, six.iterbytes(value)))


@enforce_bytes
def b58_encode(data):
    """Converts bytes data into a base 58 string."""
    data = base_to_int(data, B256)
    value = int_to_base(data, B58)

    return value


@enforce_bytes
def b58_decode(data):
    """Converts bytes data in a base 58 string into a unicode one."""
    data = base_to_int(data, B58)
    value = int_to_base(data, B256)

    return value


@enforce_bytes
def b58c_encode(data, version=b'\x00'):
    """Converts bytes data into a base 58 check string.

    WTF is Base 58 Check encoding? See here:
        https://en.bitcoin.it/wiki/Base58Check_encoding

    """
    data = version + data
    data_without_zeros = data.lstrip(b'\x00')
    nb_zeros = len(data) - len(data_without_zeros)

    double_hash = double_sha256(data)
    data = data + double_hash[0:4]
    number = bytes_to_int(data)

    b58 = int_to_base(number, B58)
    return (b'1' * nb_zeros) + b58


@enforce_bytes
def b58c_decode(data):
    data_without_ones = data.lstrip(b'1')
    nb_ones = len(data) - len(data_without_ones)

    bin = base_to_int(data, B58)
    value = b'\x00' * nb_ones + int_to_base(bin, B256)[:-4]
    b58c = b58c_encode(value, version=b'')

    if b58c != data:
        raise ValueError('%s is not a base 58 check valid value' % data)

    return value[1:]
