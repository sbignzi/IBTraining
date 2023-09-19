from tools.ib_class import ib_class
from tools.connect_to_server import connect_to_server
from tools.place_order import place_order

from tools.check_if_exist_pending_order import check_if_exist_pending_order

import os
import sys
import time

from settings import settings

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)



def read_positions(): #read all accounts positions and return DataFrame with information

    app = ib_class()    
  
    connect_to_server(app)

    symbol = 'AAPL'
    app.position_config['contract'] = settings[symbol]
    app.position_config['entryOrder']={'action':'BUY','orderType':'LMT', 'totalQuantity':2, 'lmtPrice':178 , 'transmit':False}
    app.position_config['profitOrder']={'action':'SELL','orderType':'LMT', 'totalQuantity':2, 'lmtPrice':179 , 'transmit':False}
    app.position_config['stopLossOrder']={'action':'SELL','orderType':'STOP', 'totalQuantity':2, 'auxPrice':177 , 'transmit':True}

   
     # Wait for a signal indicating that orders have been placed
    # time.sleep(1)
    # time.sleep(3)
    # Request executed orders
    app.reqPositions() # associated callback: position
    # Request non executed orders
    app.reqOpenOrders()  # Associated callback: openOrder

    # Check if a limit order exist in that level
    # isExist = check_if_exist_pending_order(app, symbol, target_price):
    # if not isExist:
    place_order(app)


 # Request open orders

    not_executed_orders = app.not_executed_orders
    print("Waiting for IB's API response for accounts positions requests...\n")
    # Needed to set timout to get opened positions (executed positions)
    time.sleep(3)
    executed_orders = app.executed_orders # associated callback: position
    # current_positions.set_index('Account',inplace=True,drop=True) #set executed_orders DataFrame index to "Account"
    print('executed_orders', executed_orders)
    print('not_executed_orders', not_executed_orders)
    
    app.disconnect()


read_positions()