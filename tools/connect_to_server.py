from threading import Thread
import time

def connect_to_server(app):

    app.connect('127.0.0.1', 7497, 0)
    #Start the socket in a thread
    api_thread = Thread(target=app.run)
    api_thread.start()
    time.sleep(0.5) #Sleep interval to allow time for connection to server

    # waiting for TWS connection 
    while(app.nextValidId == None):
        print('waiting for TWS connection')
        time.sleep(1)
        # api_thread.start()

    # Wait for the connection to be established
    # app.connection_event.wait()

    # Once the event is set, you can be sure that nextValidOrderId has been updated
    print('Connection established')