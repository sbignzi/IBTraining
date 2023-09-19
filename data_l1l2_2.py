from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import TickerId
from ibapi.contract import Contract
import pandas as pd
import datetime

class MarketDataApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.df = pd.DataFrame(columns=['Date', 'Time', 'Msec', 'Event', 'Type', 'Position', 'Operation', 'Price', 'Volume'])

    def nextValidId(self, orderId: int):
        # Request ZN market data
        contract = Contract()
        # contract.symbol = 'AAPL'
        # contract.secType = 'STK'
        # contract.currency = 'USD'
        # contract.exchange = 'SMART'
        # contract.primaryExchange = 'NASDAQ'

        contract.symbol = "ZN"
        contract.secType = "FUT"
        contract.exchange = "CBOT"
        contract.currency = "USD"
        # contract.exchange = "SMART"
        contract.lastTradeDateOrContractMonth = "202309"
        # self.reqMarketDataType(1)  # Request live data
        # self.reqMarketDataType(2)  # Request live data
        self.reqMarketDataType(3)  # Request live data

        # Request Level 2 market depth data
        self.reqMktDepth(orderId, contract, 5, isSmartDepth=False, mktDepthOptions=[])

        # Request regular market data
        self.reqMktData(orderId + 1, contract, "", False, False, [])

    def tickByTickMarketData(self, reqId: int, tickType: int, tickData: str):
        if tickType == 1:  # Bid
            tick = tickData.split(";")
            self.add_tick_data(tick, 'Bid')

        elif tickType == 2:  # Ask
            tick = tickData.split(";")
            self.add_tick_data(tick, 'Ask')

        elif tickType == 4:  # LastBid
            tick = tickData.split(";")
            self.add_tick_data(tick, 'LastBid', '')

        elif tickType == 5:  # LastAsk
            tick = tickData.split(";")
            self.add_tick_data(tick, 'LastAsk', '')

        # elif tickType == 7:  # Agression (if the agression is requested between Ask and Bid price)
        #     tick = tickData.split(";")
        #     self.add_tick_data(tick, 'Agr', '')

    def add_tick_data(self, tick, tick_type, operation='Update'):
        date_time = datetime.datetime.fromtimestamp(int(tick[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        TICK = {
            'Date': date_time.split()[0],
            'Time': date_time.split()[1],
            'Msec': int(tick[0]) % 1000,
            'Event': 'Dep' if tick_type in ['Ask', 'Bid'] else 'Agr',
            'Type': tick_type,
            'Position': tick[1],
            'Operation': operation,
            'Price': tick[2],
            'Volume': tick[3]
        }
        self.df = self.df.append(TICK, ignore_index=True)

def main():
    app = MarketDataApp()
    app.connect("127.0.0.1", 7497, clientId=0)  # Connect to TWS, adjust host and port as needed
    app.run()

    # Save the collected data to a CSV file
    app.df.to_csv("ZN_market_data.csv", index=False)
    print("Data saved to ZN_market_data.csv")

if __name__ == "__main__":
    main()
