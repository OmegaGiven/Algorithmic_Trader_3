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

    current_time = datetime.now().strftime("%H:%M:%S")
    print("Alpaca Trader activated\nCurrent Time: " + current_time)
    print("Next check to trade at: " + str(next_time(times)))

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        next_trade_time = times.pop(0)

        if current_time == next_trade_time:
            amount = float(account.buying_power) // len(stocks)
            for i in stocks:
                # try:
                trade_or_not = Alpaca_Functions.macd(i, api, 4)
                try:
                    api.get_position(i[0])
                    if trade_or_not == 'sell':
                        try:
                            Alpaca_Functions.sell(i, api, api.get_position(i).qty)
                        except:
                            continue
                except:
                    print("Dont own any of: " + i)

                if trade_or_not == 'buy':
                    quantity = Alpaca_Functions.get_quantity(i, api, amount)
                    Alpaca_Functions.buy(i, api, quantity)

                # except:
                #     print("Cannont buy right now. Maybe its a weekend")

            print("Next Trade time At: " + str(next_time(times)))
        times.append(next_trade_time)



except KeyboardInterrupt:
    print("Program Terminated, No longer trading")
    input("Press ANY key to quit")
