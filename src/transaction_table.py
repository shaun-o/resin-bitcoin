from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    value = Col('Value')
    address = Col('Address')
    
class Item(object):
    def __init__(self, value, address):
        self.value = value
        self.address = address
        

# Populate the table
def return_table(tx_list):
    items = []
    for tx in tx_list:
        items.append(dict(value=tx.value, address=tx.address))
        
    return ItemTable(items)