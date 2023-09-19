from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from tools.connect_to_server import connect_to_server
from ibapi.common import *
from ibapi.order import Order
import threading
import time
from datetime import datetime, timedelta
import logging
from settings import settings
from tools.create_contract_object import createContract


class TradingApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None
        self.position_config = {
            # 'contract':{'symbol' : 'AAPL',
            # 'secType' : 'STK',
            # 'currency' : 'USD',
            # 'exchange' : 'SMART',
            # 'primaryExchange' : 'NASDAQ'}
            }

         # Configure logging for IB API
        # logging.basicConfig(level=logging.DEBUG)
    
    # this method are trigred after calling run method
    # def error(self, reqId, errorCode, errorString):
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=None):
        print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    # this method are trigred after establishing a connection
    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

        c1 = Contract()
        c1.symbol = "ZN"
        c1.secType = "FUT"
        c1.exchange = "CBOT"
        c1.currency = "USD"
        c1.lastTradeDateOrContractMonth = "202309"

        # self.reqHistoricalData(orderId, c1, "20230310 15:00:00", "1 M", "1 hour", "TRADES", 0,1,0,[])
        # self.reqHistoricalTicks(orderId, c1,
        #                         "20230901 21:39:33 US/Central", "20230912 21:39:33 US/Central", 10, "BID_ASK", 1, True, [])
    def historicalData(self, reqId, bar):
        print(f"Historical Data:{bar}")

    def historicalTicksBidAsk(self, reqId: int, ticks: ListOfHistoricalTickBidAsk,
                                 done: bool):
        print('heloooo hist data')
        print('len(ticks)', len(ticks))
        print('type(ticks)', type(ticks))
        print('(ticks)', ticks)
        # for tick in ticks:
        #     print("HistoricalTickBidAsk. ReqId:", reqId, tick)
        # Assuming tick_data is your list of dictionaries
        if ticks:
            # Access the last tick in the list
            last_tick = ticks[-1]
            
            # Access the timestamp of the last tick
            last_timestamp = last_tick.time
            # Convert the timestamp to a datetime object
            last_datetime = datetime.fromtimestamp(last_timestamp)
            # Now, last_timestamp contains the timestamp of the last tick
            print("last_datetime:", last_datetime)
        else:
            print("The list is empty.")

        print(last_timestamp)
    
    def historicalDataEnd(self, reqId, start, end):
        print(f"End of Historical Data")
        print(f"start:{start}, end:{end}")

app=TradingApp()

connect_to_server(app)
while(app.nextValidId == None):
    print('waiting for TWS connection')
    time.sleep(1)
print('Connection established')
print('nextValidOrderId', app.nextValidOrderId)
time.sleep(1)
# Define your date range
start_date = datetime(2023, 9, 1, 21, 39, 33)
end_date = datetime(2023, 9, 3, 21, 39, 33)

# Split the date range into smaller chunks (e.g., 1000 ticks per chunk)
chunk_size = 50
current_date = start_date

symbol = 'ZN'
time_zone = settings[symbol]['contract']['timeZone']
contract = settings[symbol]['contract']
c1 = createContract(contract)

orderId = app.nextValidOrderId

# Define a starting orderId (use any number you prefer)
current_order_id = 1000

# app.run()

while current_date <= end_date:
    print('loloooooooo')
    # Calculate the end date for this chunk (e.g., 1000 ticks later)
    next_date = current_date + timedelta(minutes=1000)  # Adjust the time frame as needed
    # next_date = current_date + timedelta(milliseconds=100)  # Adjust the time frame as needed

    # print('current_date.strftime("%Y%m%d %H:%M:%S"+ America/Chicago) =====================', type(current_date.strftime("%Y%m%d %H:%M:%S"+' America/Chicago')))
    # print('current_date.strftime("%Y%m%d %H:%M:%S"+ America/Chicago) =====================', next_date.strftime("%Y%m%d %H:%M:%S")+' America/Chicago')
    # Request historical ticks for this chunk
    app.reqHistoricalTicks(current_order_id, c1, current_date.strftime("%Y%m%d %H:%M:%S"+' US/Central'), 
                            next_date.strftime("%Y%m%d %H:%M:%S")+' US/Central', chunk_size, "BID_ASK", 1, True, [])
    
    # app.reqHistoricalTicks(current_order_id, c1,
    #                             "20230901 21:39:33 US/Central", "20230912 21:39:33 US/Central", 10, "BID_ASK", 1, True, [])
   
    print('current_date', current_date)
    print('next_date', next_date)
    # Move to the next chunk
    current_date = next_date
    # current_date = lastRecordDate + timedelta(milliseconds=1000) 
    current_order_id += 1
   
    # break
    time.sleep(5)
    
app.disconnect()
# time.sleep(10)

# app.disconnect()