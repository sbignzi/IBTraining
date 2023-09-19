from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from tools.connect_to_server import connect_to_server

from threading import Thread
import time

class MyWrapper(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None

     # this method are trigred after establishing a connection
    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId
    

    def historicalData(self, reqId, bar):
        print("Historical Data. ReqId:", reqId, "Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount, "WAP:", bar.average)

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

    # Request historical data with a delay
    app.reqHistoricalData(1, contract, "", "1 D", "1 min", "TRADES", 1, 1, False, [])

    # Start the API connection in a separate thread
    api_thread = Thread(target=app.run)
    api_thread.start()

    # Wait for some time to receive historical data
    time.sleep(10)

    # Disconnect from the API
    app.disconnect()

if __name__ == "__main__":
    request_delayed_data()