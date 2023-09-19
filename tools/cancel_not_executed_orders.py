from ibapi.common import OrderId

import time

def cancel_not_executed_orders(app, symbol):

    # Wait for the connection to be established
    while app.nextValidOrderId is None:
        time.sleep(1)

    # Request open orders
    app.reqOpenOrders()  # Associated callback: openOrder

    # Wait for a moment to allow the open orders to be received
    # time.sleep(5)

    # Iterate through open orders and cancel orders for the specified symbol
    for order in app.open_orders:
        if order["symbol"] == symbol:
            order_id = OrderId(order["orderId"])
            app.cancelOrder(order_id, "")  # Pass an empty string as a placeholder
