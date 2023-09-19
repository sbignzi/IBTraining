from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading

import time
from datetime import datetime, timedelta
# import os
# import sys

# module_path = os.path.abspath(os.path.join('..'))
# if module_path not in sys.path:
#     sys.path.append(module_path)

# from settings import settings

import pandas as pd

class ib_class(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = 1000
        self.position_config = {
            # 'contract':{'symbol' : 'AAPL',
            # 'secType' : 'STK',
            # 'currency' : 'USD',
            # 'exchange' : 'SMART',
            # 'primaryExchange' : 'NASDAQ'}
            }
        
        # self.executed_orders = pd.DataFrame([], columns = ['Account','Symbol', 'Quantity', 'Average Cost', 'Sec Type', 'Direction'])
        self.executed_orders = {}
        self.not_executed_orders = []
        self.market_depth_data = []
        self.all_accounts = pd.DataFrame([], columns = ['reqId','Account', 'Tag', 'Value' , 'Currency'])
        self.connection_event = threading.Event()

    # def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
    #     print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=None):
        print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))
    # this method are trigred after establishing a connection
    # def nextValidId(self, orderId:int):
    #     print('connection')
    #     self.nextValidOrderId = orderId
    #     self.connection_event.set()
    def get_next_order_id(self):
        # Increment the order ID counter and return the next ID
        order_id = self.nextValidOrderId
        self.nextValidOrderId += 1
        return order_id
    
    def position(self, account, contract, pos, avgCost):
        # print('position ==================', pos)
        # index = str(account)+str(contract.symbol)
        # self.all_positions.loc[index]= account, contract.symbol, pos, avgCost, contract.secType
        # print('self.all_positions', self.all_positions)
        index = str(account) + str(contract.symbol)
        direction = "BUY" if pos > 0 else "SELL" if pos < 0 else "Flat"
        # "Flat" indicates no position (pos is zero)
        if str(contract.symbol) not in self.executed_orders:
            # If the index doesn't exist, create a new row
            self.executed_orders[str(contract.symbol)] = {
                "Account": account,
                "Symbol": contract.symbol,
                "Quantity": int(pos),
                "Average Cost": avgCost,
                "Sec Type": contract.secType,
                "Direction": direction
            }
        else:
            # If the index exists, update the existing row
            self.executed_orders[str(contract.symbol)]["Quantity"] = int(pos)
            self.executed_orders[str(contract.symbol)]["Average Cost"] = avgCost
            self.executed_orders[str(contract.symbol)]["Direction"] = direction
        # print('self.executed_orders', self.executed_orders)

    def openOrder(self, orderId, contract, order, orderState):
        # Check if the order is not already in the open_orders list
        if not any(o["orderId"] == orderId for o in self.not_executed_orders):
            self.not_executed_orders.append({
                "orderId": orderId,
                "symbol": contract.symbol,
                "action": order.action,
                "quantity": int(order.totalQuantity),
                "orderType": order.orderType,
                "limitPrice": order.lmtPrice,
                "stopPrice": order.auxPrice,
                "status": orderState.status
            })

    def updateMktDepth(self, reqId, position, operation, side, price, size):
        # Create a dictionary to store the market depth data for this event
        # market_depth_event = {
        #     "reqId": reqId,
        #     "position": position,
        #     "operation": operation,
        #     "side": side,
        #     "price": price,
        #     "size": size
        # }
        

        date_time = datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
        
        if position == 0:
            print('Agression =================================')
            tick_type = "lastAsk" if side == 0 else "lastBid"
            event = 'Agr'
            op = ''
        if position != 0:
            print('Depth =================================')
            tick_type = "Ask" if side == 0 else "Bid"
            event = 'Dep'
            op = 'Update'
        
        market_depth_event = {
            'Date': date_time.split()[0],
            'Time': date_time.split()[1],
            'Msec': int(time.time() * 1000) % 1000,
            'Event': event,
            'Type': tick_type,
            'Position': position,
            'Operation': op,
            'Price': price,
            'Volume': size
        }
        
        # Append the data to the list
        self.market_depth_data.append(market_depth_event)
        print(market_depth_event)

    # def updateMktDepthL2(self, reqId, position, marketMaker, operation, side, price, size, isSmartDepth):
    #     # Create a dictionary to store the market depth data for this event
    #     # market_depth_event = {
    #     #     "reqId": reqId,
    #     #     "position": position,
    #     #     "marketMaker": marketMaker,
    #     #     "operation": operation,
    #     #     "side": side,
    #     #     "price": price,
    #     #     "size": size,
    #     #     "isSmartDepth": isSmartDepth
    #     # }
    #     print('depth =================================')
    #     date_time = datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
    #     tick_type = "Ask" if side == 0 else "Bid"
        
    #     market_depth_event = {
    #         'Date': date_time.split()[0],
    #         'Time': date_time.split()[1],
    #         'Msec': int(time.time() * 1000) % 1000,
    #         'Event': 'Dep',
    #         'Type': tick_type,
    #         'Position': position,
    #         'Operation': 'Update',
    #         'Price': price,
    #         'Volume': size
    #     }
        
    #     # Append the data to the list
    #     self.market_depth_data.append(market_depth_event)
    #     print(market_depth_event)

    def accountSummary(self, reqId, account, tag, value, currency):
        index = str(account)
        self.all_accounts.loc[index]=reqId, account, tag, value, currency

