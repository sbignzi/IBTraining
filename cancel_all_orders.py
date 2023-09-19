from tools.ib_class import ib_class
from tools.connect_to_server import connect_to_server
from ibapi.common import OrderId

import os
import sys

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from settings import settings

import time

def cancel_not_executed_orders(symbols, app):
    # Iterate through open orders and cancel orders for the specified symbol
    for order in app.open_orders:
        for symbol in symbols:
            if order["symbol"] == symbol:
                order_id = OrderId(order["orderId"])
                app.cancelOrder(order_id, "")  # Pass an empty string as a placeholder

def exit_opened_orders(symbols, app):
    # Iterate through open orders and cancel orders for the specified symbol
    for symbol in symbols:
        order = app.executed_orders[symbol]
        action = order.action
        quantity = order.totalQuantity
        if action == 'BUY':
            action = 'SELL'
        else:
            action = 'BUY'
        
        Contract = settings[symbol]
        # Create a contract for the symbol
        contract = Contract()
        contract.symbol = Contract.symbol
        contract.secType = Contract.secType
        contract.currency = Contract.currency
        contract.exchange = Contract.exchange
        # Place opposit order
        # Create an opposit (close) order
        Order = Order()
        Order.action = action
        Order.totalQuantity = quantity  # Set the quantity to close
        Order.orderType = "MKT"  # Use market order to close the position
        app.placeOrder(app.nextValidOrderId, contract, Order)


app = ib_class()    

symbols = ['AAPL']

connect_to_server(app)
while not app.nextValidOrderId:
    time.sleep(1)

 # Request executed orders
app.reqPositions() # associated callback: position
# Request non executed orders
app.reqOpenOrders()  # Associated callback: openOrder

 # Request open orders

# not_executed_orders = app.not_executed_orders
print("Waiting for IB's API response for accounts positions requests...\n")
# Needed to set timout to get opened positions (executed positions)
time.sleep(3)
executed_orders = app.executed_orders # associated callback: position
# current_positions.set_index('Account',inplace=True,drop=True) #set executed_orders DataFrame index to "Account"
print('executed_orders', executed_orders)

cancel_not_executed_orders(symbols, app)
exit_opened_orders(symbols, app)