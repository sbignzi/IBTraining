from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading

class TradingApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None
    
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

        c1 = Contract()
        c1.symbol = "EUR"
        c1.secType = "CASH"
        c1.currency = "USD"
        c1.exchange = "IDEALPRO"

        self.reqMktData(1, c1, "", False, False, [])

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)

app = TradingApp()
app.connect("127.0.0.1", 7497, clientId=0)

# execute app.run in a separate thread
t = threading.Thread(target=app.run)
t.start()

# waiting for TWS connection 
while app.nextValidOrderId is None:
    print('waiting for TWS connection')

print('connection established')