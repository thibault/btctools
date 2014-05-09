"""Encoding tools.

All encoding inputs and outputs are bytes array.

"""
from __future__ import unicode_literals

import six

from crypto import double_sha256


B58 = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
B256 = b''.join([six.unichr(x) for x in range(256)])


def bytes_to_int(bytes):
    """Converts a bytes array into a big number."""
    return base_to_int(bytes, B256)


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
        number /= base

    return b''.join(value)


def b58_encode(data):
    """Converts bytes data into a base 58 string."""
    data = base_to_int(data, B256)
    value = int_to_base(data, B58)

    return value


def b58_decode(data):
    """Converts bytes data in a base 58 string into a unicode one."""
    data = base_to_int(data, B58)
    value = int_to_base(data, B256)

    return value


def b58c_encode(data, version=b'\x00'):
    """Converts bytes data into a base 58 check string.

    WTF is Base 58 Check encoding? See here:
        https://en.bitcoin.it/wiki/Base58Check_encoding

    """
    data = version + data
    data_without_zeros = data.lstrip(b'\x00')
    nb_zeros = len(data) - len(data_without_zeros)

    double_hash = double_sha256(data)
    data = data.encode('utf-8') + double_hash[0:4]
    number = bytes_to_int(data)

    b58 = int_to_base(number, B58)
    return ('1' * nb_zeros) + b58


def b58c_decode(data):
    data_without_ones = data.lstrip(b'1')
    nb_ones = len(data) - len(data_without_ones)

    bin = base_to_int(data, B58)
    value = b'\x00' * nb_ones + int_to_base(bin, B256)[:-4]
    b58c = b58c_encode(value, version='')

    if b58c != data:
        raise ValueError('%s is not a base 58 check valid value' % data)

    return value[1:]
