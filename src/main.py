import sys
from flask import Flask
import blockchain.blockexplorer


class TransactionDetails():
    def __init__(self, value, address):
        self.value = str(value).encode()
        self.address = address.encode()


def read_blockchain_address(read_address):
    address = blockchain.blockexplorer.get_address(read_address)

    transactions = address.transactions
    input_details = []
    for transaction in transactions:
        for output in transaction.outputs:
            if output.address == read_address:
                for input in transaction.inputs:
                    input_details.append(TransactionDetails(
                        input.value, input.address))
    return input_details


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Shaun This is a Raspi 3 Python Hello World!' + sys.version


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
