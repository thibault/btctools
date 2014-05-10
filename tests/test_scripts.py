from __future__ import unicode_literals

import unittest

from scripts.base import Script, PayToPubkeyScript


class ScriptsTests(unittest.TestCase):

    def setUp(self):
        self.address = '1EL3y9j8rzZwa8Hxmx2scatb3bh8KKFK6v'

    def test_stack_validity_check(self):
        with self.assertRaises(ValueError):
            ops = [1, 2, 'toto']
            Script(ops)

    def test_pay_to_pubkey_script(self):
        script = PayToPubkeyScript(self.address)
        self.assertEqual(
            script.to_hex(),
            '76a94c149234042049764dbed331c7d1fc492a4eb5007c5388ac'
        )
