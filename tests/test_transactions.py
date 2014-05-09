from __future__ import unicode_literals

import unittest

from transactions import Transaction


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
        pass


class InputTests(unittest.TestCase):
    pass
