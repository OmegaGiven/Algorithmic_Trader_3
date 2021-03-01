import alpaca_trade_api as tradeapi
import config


# checks account from API. txt so you will need the 2 security keys and the route
def getAccount():
    api = tradeapi.REST(config.key_id, config.secret_id, config.site)
    return api


def macd(symbol, api, limit_quantity):
    bar_set = api.get_barset(symbol, 'day', limit=limit_quantity)
    stock = bar_set[symbol]
    total = 0
    for x in range(limit_quantity-1):
        total += stock[x].c
    days_average = total / (limit_quantity - 1)
    current = stock[limit_quantity-1].c
    print("past day average: ", days_average)
    print("current price: ", current)
    if current > days_average * 1.05:
        return 'buy'
    else:
        return 'sell'

def margingains(symbol, api, limit_quantity):
    bar_set = api.get_barset(symbol, 'day', limit=limit_quantity)
    stock = bar_set[symbol]
    total = 0
    print(stock)
    for x in range(limit_quantity-1):
        total += stock[x].c
    days_average = total / (limit_quantity - 1)
    current = stock[limit_quantity-1].c
    print("past day average: ", days_average)
    print("current price: ", current)
    if current < days_average * 0.95:
        return 'buy'
    else:
        return 'sell'


def buy(symbol, api, quantity=1):
    api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
    # get the current price so we can display it
    bar_set = api.get_barset('AAPL', 'day', limit=1)
    stock = bar_set['AAPL']
    print('buying: ' + symbol + ' at ' + ' quantity: ' + str(quantity) + ' for : ' + str(stock[0].c))


def sell(symbol, api, quantity=1):
    api.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')
    # get the current price so we can display it
    bar_set = api.get_barset('AAPL', 'day', limit=1)
    stock = bar_set['AAPL']
    print('selling: ' + symbol + ' at ' + ' quantity: ' + str(quantity) + ' for : ' + str(stock[0].c))


def get_quantity(symbol, api, amount):
    bar_set = api.get_barset(symbol, 'day', limit=1)
    stock = bar_set[symbol]
    current = stock[0].c
    quantity = amount // current
    return quantity
