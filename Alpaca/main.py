import Account_Info, config, Alpaca_Functions
from datetime import datetime
import time as t

times = config.times  # times to check if we want to buy or not
stocks = config.stocks  # where stocks[[symbol, quantity desired]]


def next_time(times):
    current_time = datetime.now().strftime("%H:%M:%S")
    for time in times:
        hour = False
        minute = False
        second = False

        # if you want to worry about seconds for when you want to call functions
        # you will have to add it but the basics are set up for you.
        if int(time[0:2]) >= int(current_time[0:2]):
            hour = True
        if int(time[3:5]) >= int(current_time[3:5]):
            minute = True
        if int(time[6:8]) >= int(current_time[6:8]):
            second = True
        if minute and not hour:
            continue
        elif time[0:2] == current_time[0:2] and not minute:
            continue
        elif hour:
            return time
    return time[0]


try:
    api = Account_Info.getAccount()

    account = api.get_account()
    print(account)

    for x in stocks:
        try:
            current = api.get_position(x)
            print(current)
        except:
            print("No positions of: " + x)

    current_time = datetime.now().strftime("%H:%M:%S")
    print("Alpaca Trader activated\nCurrent Time: " + current_time)
    print("Next check to trade at: " + str(next_time(times)))

    while True:
        # cycles through the times you setup to check the market at those times
        # or you could be checking it as much as you want by taking out the if currtime=nexttradetime.
        current_time = datetime.now().strftime("%H:%M:%S")
        next_trade_time = times.pop(0)

        # prints account information at 8am for debugging.
        if current_time == "08:00:00":
            account = api.get_account()
            print(account)

        # if its time to trade do the following:
        if current_time == next_trade_time:
            # allocate buypower to the stocks you want. currently set to be even
            amount = float(account.buying_power) // len(stocks)

            # for every stock in your list it will check whether to buy or sell
            for i in stocks:
                # checks the barset and sees whether to buy or not.
                trade_or_not = Alpaca_Functions.macd(i, api, 1)

                # the try catch is to make sure the program doesnt end if you check your position and there is none.
                try:
                    api.get_position(i)
                    if trade_or_not == 'sell':
                        try:
                            Alpaca_Functions.sell(i, api, api.get_position(i).qty)
                        except:
                            continue
                except:
                    print("Don't own any of: " + i)

                if trade_or_not == 'buy':
                    quantity = Alpaca_Functions.get_quantity(i, api, amount)
                    Alpaca_Functions.buy(i, api, quantity)


            print("Next Trade time At: " + str(next_time(times)))
        times.append(next_trade_time)



except KeyboardInterrupt:
    print("Program Terminated, No longer trading")
    input("Press ANY key to quit")
