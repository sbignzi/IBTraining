from ibapi.contract import Contract
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from threading import Thread
from tools.connect_to_server import connect_to_server

import datetime
import time

class MyWrapper(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None

     # this method are trigred after establishing a connection
    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId
    
    def historicalData(self, reqId, bar):
        print("Received historical data:", bar)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))
    def headTimestamp(self, reqId:int, headTimestamp:str):
        print("HeadTimestamp. ReqId:", reqId, "HeadTimeStamp:", headTimestamp)

def request_delayed_data():
    app = MyWrapper()

    # Connect to the Interactive Brokers TWS or Gateway
    connect_to_server(app)
    while(app.nextValidOrderId == None):
        print('waiting for TWS connection')
        time.sleep(1)

    # Create a Contract object for ZN
    contract = Contract()
    contract.symbol = "ZN"
    contract.secType = "FUT"
    contract.exchange = "CBOT"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = "202312"

    # Define the duration and bar size for historical data
    duration = "1 D"  # 1 day of data
    bar_size = "1 min"  # 1-minute bars

    # Request historical data for ZN
    # app.reqHistoricalData(1, contract, "", duration, bar_size, "TRADES", 1, 1, False, [])
    # Start the API connection in a separate thread
    
    # api_thread = Thread(target=app.run)
    # api_thread.start()

    app.reqMktDepth(2001, contract, 5, False, [])
    app.disconnect()

if __name__ == "__main__":
    request_delayed_data()
