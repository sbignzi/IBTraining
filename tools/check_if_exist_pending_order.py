def check_if_exist_pending_order(app, symbol, target_price):

    # Iterate through open orders and check if any matches the target price
    for order in app.open_orders:
        if order["symbol"] == symbol:
            if order["orderType"] == "LMT" and order["limitPrice"] == target_price:
                print(f"Found a pending limit order for {symbol} at {target_price}")
                return True
            else: False
        else: False
            # elif order["orderType"] == "STP" and order["stopPrice"] == target_price:
            #     print(f"Found a pending stop order for {symbol} at {target_price}")
