# from ibapi.client import EClient
# from ibapi.wrapper import EWrapper
from tools.ib_class import ib_class
from ibapi.contract import Contract
from tools.connect_to_server import connect_to_server
import os
import sys
from settings import settings
from tools.create_contract_object import createContract

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


# from ibapi.common import TickTypeEnum
from ibapi.common import TickerId





import pandas as pd
import datetime
import time

# class MarketDataApp(EWrapper, EClient):
#     def __init__(self):
#         EClient.__init__(self, self)

#         self.market_depth_data = []
#         self.nextValidOrderId = None

#     def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
#         print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

#     # this method are trigred after establishing a connection
#     def nextValidId(self, orderId):
#         self.nextValidOrderId = orderId

#     def updateMktDepth(self, reqId, position, operation, side, price, size):
#         # Create a dictionary to store the market depth data for this event
#         market_depth_event = {
#             "reqId": reqId,
#             "position": position,
#             "operation": operation,
#             "side": side,
#             "price": price,
#             "size": size
#         }
        
#         # Append the data to the list
#         self.market_depth_data.append(market_depth_event)
#         print(market_depth_event)

#     def updateMktDepthL2(self, reqId, position, marketMaker, operation, side, price, size, isSmartDepth):
#         # Create a dictionary to store the market depth data for this event
#         market_depth_event = {
#             "reqId": reqId,
#             "position": position,
#             "marketMaker": marketMaker,
#             "operation": operation,
#             "side": side,
#             "price": price,
#             "size": size,
#             "isSmartDepth": isSmartDepth
#         }
        
#         # Append the data to the list
#         self.market_depth_data.append(market_depth_event)
#         print(market_depth_event)

#     def get_market_depth_data(self):
#         # Return the stored market depth data
#         return self.market_depth_data

# def main():
# app = MarketDataApp()
app = ib_class()

connect_to_server(app)
while not app.nextValidOrderId:
    time.sleep(1)    

symbol = 'ZN'
app.position_config['contract'] = settings[symbol]['contract']

contract = app.position_config['contract']
c = createContract(contract)

# contract = Contract()
# contract.symbol = "ZN"  # Replace with the symbol for ZN (10-Year Treasury Note)
# contract.secType = "FUT"
# contract.exchange = "CBOT"
# contract.lastTradeDateOrContractMonth = "202309"

app.reqMktDepth(1, c, 5, False, [])

# app.run()  # Start the event loop

# app.disconnect()  # Disconnect from IB Gateway/TWS

# Create dataframes from the collected data
market_depth_data = pd.DataFrame(app.market_depth_data, columns=["Date", "Type", "Position", "Operation", "Price", "Volume"])

# Print the dataframes or save them to a file as needed
print("market_depth_data Data:")
print(market_depth_data)


# if __name__ == "__main__":
#     main()

# if KeyboardInterrupt:
#     app.disconnect()