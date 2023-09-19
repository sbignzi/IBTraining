from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from threading import Thread
import time

class ib_class(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None
        
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

def close_long_position(symbol, quantity):
    app = ib_class()

    # Connect to the IB server
    app.connect('127.0.0.1', 7497, 0)

    # Start the socket in a thread
    api_thread = Thread(target=app.run)
    api_thread.start()
    
    # Wait for the connection to be established
    while app.nextValidOrderId is None:
        pass

    # Create a contract for the symbol
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"

    # Create a sell (close) order
    order = Order()
    order.action = "SELL"
    order.totalQuantity = quantity  # Set the quantity to close
    order.orderType = "MKT"  # Use market order to close the position

    # Place the order
    app.placeOrder(app.nextValidOrderId, contract, order)

    # Wait for a moment to allow the order to be executed
    time.sleep(5)

    # Disconnect from the IB server
    app.disconnect()

if __name__ == "__main__":
    # Specify the symbol and quantity to close
    symbol_to_close = "AAPL"
    quantity_to_close = 60  # Adjust the quantity as needed

    close_long_position(symbol_to_close, quantity_to_close)
