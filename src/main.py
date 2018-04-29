import sys
from flask import Flask
import blockchain.blockexplorer
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template


class AddressQuery(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Query')


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
    try:
        form = AddressQuery()
        # return render_template('/usr/src/app/templates/address_query.html', title='BitCoin Address', form=form)
        return render_template('address_query.html', form=form)
    except:
        print ("Unexpected error:", sys.exc_info()[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
