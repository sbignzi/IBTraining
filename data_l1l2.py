from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
# from ibapi.common import TickTypeEnum
from ibapi.common import TickerId
import pandas as pd
import datetime

class MarketDataApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        self.level_1_data = []  # List to store Level 1 market data
        self.level_2_data = []  # List to store Level 2 market data

    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice, bidSize, askSize, tickType):
        print('=================================================')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # if tickType == TickTypeEnum.BID:
        if tickType == 1:  # Bid
            self.level_1_data.append([timestamp, "Bid", 1, "Update", bidPrice, bidSize])
        # elif tickType == TickTypeEnum.ASK:
        elif tickType == 2:  # Ask
            self.level_1_data.append([timestamp, "Ask", 1, "Update", askPrice, askSize])

    def tickByTickAllLast(self, reqId, tickType, time, price, size, tickAttribLast, exchange, specialConditions):
        print('=================================================2')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # if tickType == TickTypeEnum.LAST:
        if tickType == 4 or tickType == 5:  # LastBid
            if "LastBid" in specialConditions:
                self.level_2_data.append([timestamp, "LastBid", 1, "", price, size])
            elif "LastAsk" in specialConditions:
                self.level_2_data.append([timestamp, "LastAsk", 1, "", price, size])

def main():
    app = MarketDataApp()

    app.connect("127.0.0.1", 7497, clientId=1)  # Replace with your IB Gateway/TWS IP and port
    contract = Contract()
    contract.symbol = "ZN"  # Replace with the symbol for ZN (10-Year Treasury Note)
    contract.secType = "FUT"
    contract.exchange = "CBOT"

    app.reqMarketDataType(3)  # Request Level 1 and Level 2 market data
    app.reqTickByTickData(1, contract, "BidAsk", 0, False)  # Request Bid/Ask data
    app.reqTickByTickData(2, contract, "Last", 0, False)  # Request LastBid/LastAsk data

    app.run()  # Start the event loop

    # app.disconnect()  # Disconnect from IB Gateway/TWS

    # Create dataframes from the collected data
    level_1_df = pd.DataFrame(app.level_1_data, columns=["Date", "Type", "Position", "Operation", "Price", "Volume"])
    level_2_df = pd.DataFrame(app.level_2_data, columns=["Date", "Type", "Position", "Operation", "Price", "Volume"])

    # Print the dataframes or save them to a file as needed
    print("Level 1 Market Data:")
    print(level_1_df)

    print("\nLevel 2 Market Data:")
    print(level_2_df)

if __name__ == "__main__":
    main()