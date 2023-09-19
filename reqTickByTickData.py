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

        # c1 = Contract()
        # c1.symbol = "EUR"
        # c1.secType = "CASH"
        # c1.currency = "USD"
        # c1.exchange = "IDEALPRO"

        c1 = Contract()
        c1.symbol = "ZN"
        c1.secType = "FUT"
        c1.exchange = "CBOT"
        c1.currency = "USD"
        c1.lastTradeDateOrContractMonth = "202309"

        # self.reqMktData(1, c1, "", False, False, [])
        self.reqMarketDataType(1)  # Set market data type to real-time
        self.reqMktData(1, c1, "", True, False, []) 

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)

    def tickSize(self, reqId, tickType, size):
        print("Tick Size. Ticker Id:", reqId, "tickType:", tickType, "Size:", size)

    def tickString(self, reqId, tickType, value):
        print("Tick String. Ticker Id:", reqId, "tickType:", tickType, "Value:", value)

    #  def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
    #                          bidSize: Decimal, askSize: Decimal, tickAttribBidAsk: TickAttribBidAsk):
    #          super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
    #                                 askSize, tickAttribBidAsk)
    #        print("BidAsk. ReqId:", reqId,
    #              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"),
    #              "BidPrice:", floatMaxString(bidPrice), "AskPrice:", floatMaxString(askPrice), "BidSize:", decimalMaxString(bidSize),
    #              "AskSize:", decimalMaxString(askSize), "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:", tickAttribBidAsk.askPastHigh)
app = TradingApp()
app.connect("127.0.0.1", 7497, clientId=0)

# execute app.run in a separate thread
t = threading.Thread(target=app.run)
t.start()

# waiting for TWS connection 
while app.nextValidOrderId is None:
    print('waiting for TWS connection')
    # time.sleep(1)

print('connection established')