from __future__ import unicode_literals

import six

from scripts import constants as C
from encoding import (
    b58c_decode, bytes_to_hex, little_endian_uint8, little_endian_uint16,
    little_endian_uint32
)


class Script(object):
    """Script management class."""

    def __init__(self, stack):
        """Initiates a script object.

        One must pass a list of operations or variables to be added to the stack.

        Each element of the list can be:
         * a single byte, representing a single op
         * a bytes array, representing a constant to be pushed on the script stack.

        Use scripts constants:

            >>> from scripts.constants import (
            ...     OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
            ... )

        Then create the script stack:

            >>> address = '1EL3y9j8rzZwa8Hxmx2scatb3bh8KKFK6v'.encode('utf-8')
            >>> ops = [
            ...     OP_DUP,
            ...     OP_HASH160,
            ...     address,
            ...     OP_EQUALVERIFY,
            ...     OP_CHECKSIG,
            ... ]
            >>> script = Script(ops)

        """
        if self.is_stack_valid(stack):
            self.stack = stack
        else:
            raise ValueError('The script stack can only contains single ints or bytes arrays')

    def is_stack_valid(self, stack):
        """Checks that all ops in the given stack are valid."""

        def is_op_valid(op):
            return isinstance(op, int) or isinstance(op, six.binary_type)

        validity_list = map(is_op_valid, stack)
        return all(validity_list)

    def push_constant(self, bytes):
        """Converts a string to a pushdata operation."""
        str_len = len(bytes)

        if str_len <= 0xff:
            push_code = C.OP_PUSHDATA1
            bin_len = little_endian_uint8(str_len)
        elif str_len <= 0xffff:
            push_code = C.OP_PUSHDATA2
            bin_len = little_endian_uint16(str_len)
        elif str_len <= 0xffffffff:
            push_code = C.OP_PUSHDATA4
            bin_len = little_endian_uint32(str_len)
        else:
            raise ValueError('The content to push is too big')

        return b''.join([
            six.int2byte(push_code),
            bin_len,
            bytes
        ])

    def to_bin(self):
        """Converts the stack to a binary value."""

        def push_op(op):
            if isinstance(op, int):
                op = six.int2byte(op)
            else:
                op = self.push_constant(op)
            return op

        bin_script = b''.join(map(push_op, self.stack))
        return bin_script

    def to_hex(self):
        """Converts the string to an hexadecimal string."""
        bin_script = self.to_bin()
        script = bytes_to_hex(bin_script)
        return script

    def __len__(self):
        return len(self.to_bin())


class PayToPubkeyScript(Script):

    def __init__(self, address):
        bin_address = b58c_decode(address.encode('ascii'))

        ops = [
            C.OP_DUP,
            C.OP_HASH160,
            bin_address,
            C.OP_EQUALVERIFY,
            C.OP_CHECKSIG,
        ]
        return super(PayToPubkeyScript, self).__init__(ops)
