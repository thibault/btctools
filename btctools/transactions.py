class Input:
    def __init__(self, tx_hash, output_id):
        self.tx_hash = tx_hash
        self.output_id = output_id


class Output:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount


class BaseTransaction:
    """A Bitcoin transaction.

    There are different standard transaction. Every one of them is defined
    in a custom subclass of this base class.

    More info on a transaction data format:

        https://en.bitcoin.it/wiki/Transactions
        https://en.bitcoin.it/w/images/en/e/e1/TxBinaryMap.png

    """
    VERSION = 1

    def __init__(self, inputs=[], outputs=[]):
        """Creates a transaction object.

        Inputs are a list of (<transaction hash>, <output id>) tuples.
        Outputs are a list of (<address>, <amount>) tuples.

        """
        self.inputs = [Input(*i) for i in inputs]
        self.outputs = [Output(*o) for o in outputs]

    @property
    def in_counter(self):
        return len(self.inputs)

    @property
    def out_counter(self):
        return len(self.outputs)


class PayToPubkeyTransaction(BaseTransaction):
    pass


# The default transaction is a Pay to Pubkey one
Transaction = PayToPubkeyTransaction


class P2SHTransaction(BaseTransaction):
    pass
