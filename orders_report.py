from tools.ib_class import ib_class
from tools.connect_to_server import connect_to_server

import time

def orders_report(): #read all accounts positions and return DataFrame with information

    app = ib_class()    
  
    connect_to_server(app)
    while not app.nextValidOrderId:
        time.sleep(1)

  
     # Wait for a signal indicating that orders have been placed
    # time.sleep(1)
    # time.sleep(3)
    # Request executed orders
    app.reqPositions() # associated callback: position
    # Request non executed orders
    app.reqOpenOrders()  # Associated callback: openOrder

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


orders_report()