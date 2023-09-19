from ibapi.contract import Contract

def createContract(contract):
    c = Contract()
    c.symbol = contract['symbol']
    c.secType = contract['secType']
    c.currency = contract['currency']
    c.exchange = contract['exchange']
    if 'primaryExchange' in contract:
        c.primaryExchange = contract['primaryExchange']
    if 'lastTradeDateOrContractMonth' in contract:
         c.lastTradeDateOrContractMonth = contract['lastTradeDateOrContractMonth']
    return c