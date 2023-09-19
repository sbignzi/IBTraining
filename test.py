from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import TickerId
from ibapi.contract import Contract
from ibapi.order import Order


from threading import Thread

import pandas as pd
import time

class ib_class(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None
        
        self.all_positions = pd.DataFrame([], columns = ['Account','Symbol', 'Quantity', 'Average Cost', 'Sec Type', 'Direction'])
        self.all_accounts = pd.DataFrame([], columns = ['reqId','Account', 'Tag', 'Value' , 'Currency'])

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    # this method are trigred after establishing a connection
    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

    def position(self, account, contract, pos, avgCost):
        print('position ==================')
        print('position ==================', pos)
        # index = str(account)+str(contract.symbol)
        # self.all_positions.loc[index]= account, contract.symbol, pos, avgCost, contract.secType
        # print('self.all_positions', self.all_positions)
        index = str(account) + str(contract.symbol)
        direction = "BUY" if pos > 0 else "SELL" if pos < 0 else "Flat"
        # "Flat" indicates no position (pos is zero)
        if index not in self.all_positions.index:
            # If the index doesn't exist, create a new row
            self.all_positions.loc[index] = {
                "Account": account,
                "Symbol": contract.symbol,
                "Quantity": pos,
                "Average Cost": avgCost,
                "Sec Type": contract.secType,
                "Direction": direction
            }
        else:
            # If the index exists, update the existing row
            self.all_positions.at[index, "Quantity"] = pos
            self.all_positions.at[index, "Average Cost"] = avgCost
            self.all_positions.at[index, "Direction"] = direction
        print('self.all_positions', self.all_positions)

    def accountSummary(self, reqId, account, tag, value, currency):
        index = str(account)
        self.all_accounts.loc[index]=reqId, account, tag, value, currency

def place_order(app):
    # define Apple etock contract
    c1 = Contract()

    c1.symbol = 'AAPL'
    c1.secType = 'STK'
    c1.currency = 'USD'
    c1.exchange = 'SMART'
    c1.primaryExchange = 'NASDAQ'

    orderId = app.nextValidOrderId 
    # orderId = 1

    # create the entry order
    entryOrder = Order()

    entryOrder.orderId = orderId
    entryOrder.action = 'BUY'
    # entryOrder.action = 'SELL'
    entryOrder.orderType = 'LMT'
    # entryOrder.orderType = 'MKT'
    entryOrder.totalQuantity = 10
    # entryOrder.lmtPrice = 140
    entryOrder.lmtPrice = 178
    entryOrder.transmit = False

    # create the profit order
    profitOrder = Order()

    profitOrder.orderId = orderId + 1
    profitOrder.parentId = entryOrder.orderId
    profitOrder.action = 'SELL'
    profitOrder.orderType = 'LMT'
    profitOrder.totalQuantity = 10
    profitOrder.lmtPrice = 141
    profitOrder.lmtPrice = 179
    profitOrder.transmit = False

    # create the stop loss order
    stopLossOrder = Order()

    stopLossOrder.orderId = orderId + 2
    stopLossOrder.parentId = entryOrder.orderId
    stopLossOrder.action = 'SELL'
    stopLossOrder.orderType = 'STOP'
    stopLossOrder.totalQuantity = 10
    stopLossOrder.auxPrice = 177
    stopLossOrder.transmit = True

    # place an order
    app.placeOrder(orderId, c1, entryOrder)
    app.placeOrder(orderId+1, c1, profitOrder)
    app.placeOrder(orderId+2, c1, stopLossOrder)

def connect_to_server(app):

    app.connect('127.0.0.1', 7497, 0)
    #Start the socket in a thread
    api_thread = Thread(target=app.run)
    api_thread.start()
    time.sleep(0.5) #Sleep interval to allow time for connection to server

    # waiting for TWS connection 
    while(app.nextValidOrderId == None):
        print('waiting for TWS connection')

    print('connection established')

def read_positions(): #read all accounts positions and return DataFrame with information

    app = ib_class()    
  
    

    connect_to_server(app)
    time.sleep(3)
    place_order(app)
     # Wait for a signal indicating that orders have been placed
    while not app.nextValidOrderId:
        time.sleep(1)
    # time.sleep(3)
    app.reqPositions() # associated callback: position
 # Request open orders (pending orders)
    # app.reqOpenOrders()  # Associated callback: openOrder
    # app.cancelPositions()
    print("Waiting for IB's API response for accounts positions requests...\n")
    time.sleep(3)
    current_positions = app.all_positions # associated callback: position
    current_positions.set_index('Account',inplace=True,drop=True) #set all_positions DataFrame index to "Account"
    print('current_positions', current_positions)
    
    app.disconnect()

    return(current_positions)

read_positions()