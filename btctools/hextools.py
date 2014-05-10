from __future__ import unicode_literals

import binascii

from struct import pack
from encoding import bytes_to_hex


def little_endian_varint(integer):
    """Convert an integer to the Bitcoin variable length integer.

    See here for the protocol specification:
        https://en.bitcoin.it/wiki/Protocol_specification#Variable_length_integer

    See here for the `struct.pack` format options:
        https://docs.python.org/2/library/struct.html#format-characters

    """
    if integer < 0xfd:
        prefix = b''
        format = b'<B'
    elif integer <= 0xffff:
        prefix = b'\xfd'
        format = b'<H'
    elif integer <= 0xffffffff:
        prefix = b'\xfe'
        format = b'<I'
    else:
        prefix = b'\xff'
        format = b'<Q'

    return bytes_to_hex(prefix + pack(format, integer))


def little_endian_uint8(int8):
    """Convert an integer into a 1 byte little endian hexa string."""
    return bytes_to_hex(pack(b'<B', int8))


def little_endian_uint16(int16):
    """Convert an integer into a 2 bytes little endian hexa string."""
    return bytes_to_hex(pack(b'<H', int16))


def little_endian_uint32(int32):
    """Convert an integer into a 4 bytes little endian hexa string."""
    return bytes_to_hex(pack(b'<I', int32))


def little_endian_uint64(int32):
    """Convert an integer into a 8 bytes little endian hexa string."""
    return bytes_to_hex(pack(b'<Q', int32))


def little_endian_str(string):
    return bytes_to_hex(string[::-1])


def little_endian_hex(hexa):
    data = binascii.unhexlify(hexa)
    return bytes_to_hex(data[::-1])
