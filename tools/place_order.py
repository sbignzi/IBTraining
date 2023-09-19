from ibapi.contract import Contract
from ibapi.order import Order
from .create_contract_object import createContract
def place_order(app):
    # define Apple etock contract
    contract, entry_order = app.position_config['contract']['contract'], app.position_config['entryOrder']
    if 'profitOrder' in app.position_config:
        profit_order = app.position_config['profitOrder']
    if 'stopLossOrder' in app.position_config:
        stop_loss_order = app.position_config['stopLossOrder']
    # c1 = Contract()
    # c1.symbol = contract['symbol']
    # c1.secType = contract['secType']
    # c1.currency = contract['currency']
    # c1.exchange = contract['exchange']
    # if 'primaryExchange' in contract:
    #     c1.primaryExchange = contract['primaryExchange']
    # if 'lastTradeDateOrContractMonth' in contract:
    #      c1.lastTradeDateOrContractMonth = contract['lastTradeDateOrContractMonth']
    c1 = createContract(contract)
    # orderId = app.nextValidOrderId 
    # orderId = app.get_next_order_id() 
    orderId = app.nextValidOrderId
    print('orderId', orderId)
    # orderId = 1

    # create the entry order
    entryOrder = Order()

    entryOrder.orderId = orderId
    entryOrder.action = entry_order['action']
    # entryOrder.action = 'SELL'
    entryOrder.orderType = entry_order['orderType']
    # entryOrder.orderType = 'MKT'
    entryOrder.totalQuantity = entry_order['totalQuantity']
    # entryOrder.lmtPrice = 140
    entryOrder.lmtPrice = entry_order['lmtPrice']
    entryOrder.transmit = entry_order['transmit']
    entryOrder.eTradeOnly=''
    entryOrder.firmQuoteOnly=''

    if 'profitOrder' in app.position_config:
        # create the profit order
        profitOrder = Order()

        profitOrder.orderId = orderId + 1
        profitOrder.parentId = entryOrder.orderId
        profitOrder.action = profit_order['action']
        profitOrder.orderType = profit_order['orderType']
        profitOrder.totalQuantity = profit_order['totalQuantity']
        # profitOrder.lmtPrice = 141
        profitOrder.lmtPrice = profit_order['lmtPrice']
        profitOrder.transmit = profit_order['transmit']
        profitOrder.eTradeOnly=''
        profitOrder.firmQuoteOnly=''
    if 'stopLossOrder' in app.position_config:
        # create the stop loss order
        stopLossOrder = Order()

        stopLossOrder.orderId = orderId + 2
        stopLossOrder.parentId = entryOrder.orderId
        stopLossOrder.action = stop_loss_order['action']
        stopLossOrder.orderType = stop_loss_order['orderType']
        stopLossOrder.totalQuantity = stop_loss_order['totalQuantity']
        stopLossOrder.auxPrice = stop_loss_order['auxPrice']
        stopLossOrder.transmit = stop_loss_order['transmit']
        stopLossOrder.eTradeOnly=''
        stopLossOrder.firmQuoteOnly=''

    # place an order
    app.placeOrder(orderId, c1, entryOrder)
    if 'profitOrder' in app.position_config:
        app.placeOrder(orderId+1, c1, profitOrder)
    if 'stopLossOrder' in app.position_config:
        app.placeOrder(orderId+2, c1, stopLossOrder)