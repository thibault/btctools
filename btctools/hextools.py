from __future__ import unicode_literals

from struct import pack


def little_endian_varint(integer):
    """Convert an integer to the Bitcoin variable length integer.

    See here for the protocol specification:
        https://en.bitcoin.it/wiki/Protocol_specification#Variable_length_integer

    See here for the `struct.pack` format options:
        https://docs.python.org/2/library/struct.html#format-characters

    """
    if integer < 0xfd:
        prefix = ''
        format = b'<B'
    elif integer <= 0xffff:
        prefix = 'fd'
        format = b'<H'
    elif integer <= 0xffffffff:
        prefix = 'fe'
        format = b'<I'
    else:
        prefix = 'ff'
        format = b'<Q'

    return prefix + pack(format, integer).encode('hex')


def little_endian_uint8(int8):
    """Convert an integer into a 1 byte little endian hexa string."""
    return pack(b'<B', int8).encode('hex')


def little_endian_uint16(int16):
    """Convert an integer into a 2 bytes little endian hexa string."""
    return pack(b'<H', int16).encode('hex')


def little_endian_uint32(int32):
    """Convert an integer into a 4 bytes little endian hexa string."""
    return pack(b'<I', int32).encode('hex')


def little_endian_uint64(int32):
    """Convert an integer into a 8 bytes little endian hexa string."""
    return pack(b'<Q', int32).encode('hex')


def little_endian_str(string):
    return string[::-1].encode('hex')


def little_endian_hex(hexa):
    return hexa.decode('hex')[::-1].encode('hex')
