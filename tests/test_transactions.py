from __future__ import unicode_literals

import unittest

from transactions import Transaction
from keys import get_key_from_hex


class TransactionTests(unittest.TestCase):

    def setUp(self):
        inputs = [
            ('b0ff74bb0dd894797153ccb862c9f9a488e657452647ada440fe1006ece95c78', 0),
            ('683d180645632d45f23baf2fb2897241321c1af779f3064ebd24aa517bae6a22', 0),
        ]

        outputs = [
            ('1EL3y9j8rzZwa8Hxmx2scatb3bh8KKFK6v', 1000),
            ('115MDLurYMiExVwfTU7R4kE43zrdVoC2pz', 49585000),
        ]

        self.tx = Transaction(inputs, outputs)

    def test_transaction_in_and_out_counters(self):
        self.assertEqual(self.tx.in_counter, 2)
        self.assertEqual(self.tx.out_counter, 2)

    def test_transaction_input_constructor(self):
        self.assertEqual(
            self.tx.inputs[0].tx_hash,
            'b0ff74bb0dd894797153ccb862c9f9a488e657452647ada440fe1006ece95c78'
        )
        self.assertEqual(self.tx.inputs[0].output_id, 0)

    def test_transaction_output_constructor(self):
        self.assertEqual(
            self.tx.outputs[0].address,
            '1EL3y9j8rzZwa8Hxmx2scatb3bh8KKFK6v'
        )
        self.assertEqual(self.tx.outputs[0].amount, 1000)

    def test_transaction_to_hex(self):
        self.assertEqual(
            self.tx.to_hex(),
            '0100000002785ce9ec0610fe40a4ad47264557e688a4f9c962b8cc53717994d80dbb74ffb00000000000ffffffff226aae7b51aa24bd4e06f379f71a1c32417289b22faf3bf2452d634506183d680000000000ffffffff02e8030000000000001a76a94c149234042049764dbed331c7d1fc492a4eb5007c5388ac689bf402000000001a76a94c1400d289624679d48aae98137561f1f9df60791a7c88ac00000000'
        )


class SigningTests(unittest.TestCase):

    def setUp(self):
        hexa = '0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D'
        self.key = get_key_from_hex(hexa)

    def test_signing_simple_transaction(self):
        inputs = [
            ('b0ff74bb0dd894797153ccb862c9f9a488e657452647ada440fe1006ece95c78', 0),
        ]

        outputs = [
            ('115MDLurYMiExVwfTU7R4kE43zrdVoC2pz', 50000000),
        ]

        tx = Transaction(inputs, outputs)
        txCopy = tx.generate_signing_form(0, self.key)
