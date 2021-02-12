import alpaca_trade_api as tradeapi


def macd(symbol, api, limit_quantity):
    bar_set = api.get_barset(symbol, 'day', limit=limit_quantity)
    stock = bar_set[symbol]
    day1 = stock[0].c
    day2 = stock[1].c
    day3 = stock[2].c
    days_average = (day1 + day2 + day3) / 3
    current = stock[3].o
    if current > days_average * 0.9:
        return 'buy'
    else:
        return 'sell'


def buy(symbol, api, quantity=1):
    api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
    print('buying: ' + symbol + ' at ' + ' quantity: ' + str(quantity) + ' for : ')


def sell(symbol, api, quantity=1):
    api.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')
    print('selling: ' + symbol + ' at ' + ' quantity: ' + str(quantity) + ' for : ')


def get_quantity(symbol, api, amount):
    bar_set = api.get_barset(symbol, 'day', limit=1)
    stock = bar_set[symbol]
    current = stock[0].o
    quantity = amount // current
    return quantity
