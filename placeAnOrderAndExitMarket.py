from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.ticktype import TickTypeEnum

class MyWrapper(EWrapper):
    def __init__(self):
        super().__init__()

    def nextValidId(self, orderId: int):
        self.orderId = orderId

# A tick price represents a specific price data point for a financial instrument, such as the bid price, ask price, last traded price, etc.
    def tickPrice(self, reqId, tickType, price, attrib):
        if reqId == 1 and tickType == TickTypeEnum.BID and price >= 101:
            self.place_exit_order()

    def place_exit_order(self):
        exit_order = Order()
        exit_order.action = "SELL"
        exit_order.orderType = "MKT"
        exit_order.totalQuantity = 100

        app.placeOrder(app.orderId + 1, contract, exit_order)

class IBClient(EClient):
    def __init__(self, wrapper):
        super().__init__(wrapper)

def place_limit_and_exit():
    global app
    app = IBClient(MyWrapper())
    app.connect("127.0.0.1", 7497, clientId=1)  # Replace with appropriate IP and port

    global contract
    contract = Contract()
    contract.symbol = "AAPL"  # Replace with the desired symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    limit_order = Order()
    limit_order.action = "BUY"
    limit_order.orderType = "LMT"
    limit_order.totalQuantity = 100
    limit_order.lmtPrice = 100  # Limit buy price

    app.reqIds(-1)  # Request order IDs
    app.reqMarketDataType(4)  # Request real-time market data (delayed)
    app.reqMktData(1, contract, "", False, False, [])  # Subscribe to market data
    app.run()

    limit_order.orderId = app.orderId
    app.placeOrder(limit_order.orderId, contract, limit_order)

    app.disconnect()

if __name__ == "__main__":
    place_limit_and_exit()
