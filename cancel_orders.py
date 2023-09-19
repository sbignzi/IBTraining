from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from threading import Thread

class ib_class(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None
        
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    # This method is triggered after establishing a connection
    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

def cancel_all_orders():
    app = ib_class()

    # Connect to the IB server
    app.connect('127.0.0.1', 7497, 0)

    # Start the socket in a thread
    api_thread = Thread(target=app.run)
    api_thread.start()
    
    # Wait for the connection to be established
    while app.nextValidOrderId is None:
        pass

    print('connection established')

    # Cancel all open orders
    app.cancelPositions()
    # app.reqGlobalCancel()

    # Wait for a moment to allow the orders to be canceled
    import time
    time.sleep(2)

    # Disconnect from the IB server
    app.disconnect()

if __name__ == "__main__":
    cancel_all_orders()
