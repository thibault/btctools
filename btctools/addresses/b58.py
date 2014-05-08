from __future__ import unicode_literals

import six


B58 = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
B256 = b''.join([six.unichr(x) for x in range(256)])


def to_bin(string, base_str):
    """Converts an unicode value into a number."""
    string = string.encode('utf-8')  # convert to bytes
    value = 0
    base = len(base_str)
    for b in string:
        value *= base
        value += base_str.find(b)

    return value


def to_base(number, base_str):
    """Converts a number into a string encoded in the given base."""
    value = []
    base = len(base_str)
    while number > 0:
        value = [base_str[number % base]] + value
        number -= number % base
        number /= base

    return b''.join(value).decode('utf-8')


def b58_encode(data):
    """Converts unicode data into a base 58 string."""
    data = to_bin(data, B256)
    value = to_base(data, B58)

    return value


def b58_decode(data):
    """Converts a base 58 string into a unicode one."""
    data = to_bin(data, B58)
    value = to_base(data, B256)

    return value


def b58c_encode(data):
    """Converts unicode data into a base 58 check string.

    WTF is Base 58 Check encoding? See here:
        https://en.bitcoin.it/wiki/Base58Check_encoding

    """
    pass


def b58c_decode(data):
    pass
