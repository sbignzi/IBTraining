from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from tools.connect_to_server import connect_to_server

from threading import Thread
import time

class MyWrapper(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        self.market_depth_data = []
        self.nextValidOrderId = None

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    # this method are trigred after establishing a connection
    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

    def updateMktDepth(self, reqId, position, operation, side, price, size):
        # Create a dictionary to store the market depth data for this event
        market_depth_event = {
            "reqId": reqId,
            "position": position,
            "operation": operation,
            "side": side,
            "price": price,
            "size": size
        }
        
        # Append the data to the list
        self.market_depth_data.append(market_depth_event)
        print(market_depth_event)


    def updateMktDepthL2(self, reqId, position, marketMaker, operation, side, price, size, isSmartDepth):
        # Create a dictionary to store the market depth data for this event
        market_depth_event = {
            "reqId": reqId,
            "position": position,
            "marketMaker": marketMaker,
            "operation": operation,
            "side": side,
            "price": price,
            "size": size,
            "isSmartDepth": isSmartDepth
        }
        
        # Append the data to the list
        self.market_depth_data.append(market_depth_event)
        print(market_depth_event)

    def get_market_depth_data(self):
        # Return the stored market depth data
        return self.market_depth_data
    
def request_delayed_data():
    app = MyWrapper()

    # Connect to the Interactive Brokers TWS or Gateway
    connect_to_server(app)
    while(app.nextValidOrderId == None):
        print('waiting for TWS connection')
        time.sleep(1)
    # Define the contract for ZN (10-Year Treasury Note)
    contract = Contract()
    contract.symbol = "ZN"
    contract.secType = "FUT"
    contract.exchange = "CBOT"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = "202309"

    # app.reqMarketDataType(3)
    app.reqMktDepth(1, contract, 5, False, [])

    # app.disconnect()

if __name__ == "__main__":
    request_delayed_data()