from __future__ import unicode_literals

import six

from crypto import double_sha256, bytes_to_int


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

    return b''.join(value)


def b58_encode(data):
    """Converts unicode data into a base 58 string."""
    data = to_bin(data, B256)
    value = to_base(data, B58)

    return value.decode('utf-8')


def b58_decode(data):
    """Converts a base 58 string into a unicode one."""
    data = to_bin(data, B58)
    value = to_base(data, B256)

    return value.decode('utf-8')


def b58c_encode(data, version='\x00'):
    """Converts unicode data into a base 58 check string.

    WTF is Base 58 Check encoding? See here:
        https://en.bitcoin.it/wiki/Base58Check_encoding

    """
    data = version + data
    data_without_zeros = data.lstrip(b'\x00')
    nb_zeros = len(data) - len(data_without_zeros)

    double_hash = double_sha256(data)
    data = data.encode('utf-8') + double_hash[0:4]
    number = bytes_to_int(data)

    b58 = to_base(number, B58)
    return ('1' * nb_zeros) + b58


def b58c_decode(data):
    data_without_ones = data.lstrip('1')
    nb_ones = len(data) - len(data_without_ones)

    bin = to_bin(data, B58)
    value = '\x00' * nb_ones + to_base(bin, B256)[:-4]
    b58c = b58c_encode(value, version='')

    if b58c != data:
        raise ValueError('%s is not a base 58 check valid value' % data)

    return value[1:]
