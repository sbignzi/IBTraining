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

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=None):
        print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

    def historicalData(self, reqId, bar):
        print(f"Historical Data:{bar}")

    def historicalTicksBidAsk(self, reqId: int, ticks: ListOfHistoricalTickBidAsk, done: bool):
        print('Historical Ticks Bid Ask:')
        print('Number of Ticks:', len(ticks))
        if ticks:
            last_tick = ticks[-1]
            last_timestamp = last_tick.time
            last_datetime = datetime.fromtimestamp(last_timestamp)
            print("Last Tick Timestamp:", last_datetime)
        else:
            print("The list is empty.")

    def historicalDataEnd(self, reqId, start, end):
        print(f"End of Historical Data")
        print(f"Start: {start}, End: {end}")

app = TradingApp()

connect_to_server(app)
while app.nextValidId is None:
    print('Waiting for TWS connection')
    time.sleep(1)
print('Connection established')
print('Next Valid Order ID:', app.nextValidOrderId)
time.sleep(1)

# Define your date range
start_date = datetime(2023, 9, 1, 21, 39, 33)
end_date = datetime(2023, 9, 3, 21, 39, 33)

# Reduce the chunk size and add delays
chunk_size = 20
current_date = start_date
# c1 = Contract()
# c1.symbol = "ZN"
# c1.secType = "FUT"
# c1.exchange = "CBOT"
# c1.currency = "USD"
# c1.lastTradeDateOrContractMonth = "202309"

symbol = 'ZN'
time_zone = settings[symbol]['contract']['timeZone']
contract = settings[symbol]['contract']
c1 = createContract(contract)

orderId = app.nextValidOrderId
current_order_id = 1000

while current_date <= end_date:
    print('Requesting Historical Data...')
    next_date = current_date + timedelta(minutes=1000)

    # Request historical ticks for this chunk
    app.reqHistoricalTicks(orderId, c1, current_date.strftime("%Y%m%d %H:%M:%S") + ' US/Central',
                            next_date.strftime("%Y%m%d %H:%M:%S") + ' US/Central', chunk_size, "BID_ASK", 1, True, [])

    print('Current Date:', current_date)
    print('Next Date:', next_date)

    current_date = next_date
    current_order_id += 1

    # Add a delay between requests to avoid pacing violations
    time.sleep(15)

app.disconnect()
