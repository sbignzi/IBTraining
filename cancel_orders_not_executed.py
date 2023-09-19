from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import OrderId
from threading import Thread

class ib_class(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None
        self.open_orders = []

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

    def openOrder(self, orderId, contract, order, orderState):
        self.open_orders.append({
            "orderId": orderId,
            "symbol": contract.symbol,
            "status": orderState.status
        })

def cancel_pending_orders(symbol):
    app = ib_class()

    # Connect to the IB server
    app.connect('127.0.0.1', 7497, 0)

    # Start the socket in a thread
    api_thread = Thread(target=app.run)
    api_thread.start()
    
    # Wait for the connection to be established
    while app.nextValidOrderId is None:
        pass

    # Request open orders
    app.reqOpenOrders()  # Associated callback: openOrder

    # Wait for a moment to allow the open orders to be received
    import time
    time.sleep(5)

    # Iterate through open orders and cancel orders for the specified symbol
    for order in app.open_orders:
        if order["symbol"] == symbol:
            order_id = OrderId(order["orderId"])
            app.cancelOrder(order_id, "")  # Pass an empty string as a placeholder

    # Disconnect from the IB server
    app.disconnect()

if __name__ == "__main__":
    # Specify the symbol for which you want to cancel orders
    symbol_to_cancel = "AAPL"  # Adjust the symbol as needed

    cancel_pending_orders(symbol_to_cancel)
