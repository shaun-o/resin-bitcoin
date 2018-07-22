import sys
import os
from flask import Flask, request, render_template, flash
import blockchain.blockexplorer
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Label
from wtforms.validators import DataRequired
import transaction_table
import redis

r = redis.StrictRedis(host=os.environ['redis'], port=6379, db=0)
r.set('count', '0')

from flask_app import app
from celery_app import celery
from tasks import add_together

class AddressQuery(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    visitor_count = Label('test', 'Caption')
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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print ('In the base route')
    print ('Request method is %s ' % request.method)
    form = AddressQuery(request.form)
    flash(form.errors)
    if request.method == 'POST':
        print ('In the post branch')
        tx_list = read_blockchain_address(form.address.data)
        return transaction_table.return_table(tx_list).__html__()
    print ('In the get branch')
    r.incr('count')
    form.visitor_count.text = str(r.get('count'), 'utf-8')
    return render_template('address_query.html', form=form)
    
@app.route('/celery', methods=['GET'])
def run_celery_task():
    result = add_together.delay(23, 42)
    return str(result.wait())


if __name__ == '__main__':
    print('In main')
    port = os.environ['PORT']

    app.run(host='0.0.0.0', port=int(port))
