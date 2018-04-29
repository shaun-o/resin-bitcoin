import sys
import os
from flask import Flask, request
import blockchain.blockexplorer
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template
import traceback


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
app.debug = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print ('In the base route')
    print ('Request method is %s ' % request.method)
    form = AddressQuery()
    if form.validate_on_submit():
        print ('In the post branch')
        return 'Submitted request for address {}'.format(
            form.address.data)
    print ('In the get branch')
    return render_template('address_query.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
