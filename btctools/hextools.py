from struct import pack


def var_length_int(integer):
    """Convert an integer to the Bitcoin variable length integer.

    See here for the protocol specification:
        https://en.bitcoin.it/wiki/Protocol_specification#Variable_length_integer

    See here for the `struct.pack` format options:
        https://docs.python.org/2/library/struct.html#format-characters

    """
    if integer < 0xfd:
        prefix = ''
        format = '<B'
    elif integer <= 0xffff:
        prefix = 'fd'
        format = '<H'
    elif integer <= 0xffffffff:
        prefix = 'fe'
        format = '<I'
    else:
        prefix = 'ff'
        format = '<Q'

    return prefix + pack(format, integer).encode('hex')
