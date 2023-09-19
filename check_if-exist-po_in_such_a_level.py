from ibapi.client import EClient
from ibapi.wrapper import EWrapper
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
        # Check if the order is not already in the open_orders list
        if not any(o["orderId"] == orderId for o in self.open_orders):
            self.open_orders.append({
                "orderId": orderId,
                "symbol": contract.symbol,
                "action": order.action,
                "quantity": order.totalQuantity,
                "orderType": order.orderType,
                "limitPrice": order.lmtPrice,
                "stopPrice": order.auxPrice,
                "status": orderState.status
            })

def check_pending_order(symbol, target_price):
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

    # Iterate through open orders and check if any matches the target price
    for order in app.open_orders:

        if order["symbol"] == symbol:
            if order["orderType"] == "LMT" and order["limitPrice"] == target_price:
                print(f"Found a pending limit order for {symbol} at {target_price}")
            elif order["orderType"] == "STP" and order["stopPrice"] == target_price:
                print(f"Found a pending stop order for {symbol} at {target_price}")
    print('app.open_orders', app.open_orders)
    # Disconnect from the IB server
    app.disconnect()

if __name__ == "__main__":
    # Specify the symbol and target price to check
    symbol_to_check = "AAPL"
    target_price_to_check = 140.0  # Adjust the target price as needed

    check_pending_order(symbol_to_check, target_price_to_check)
