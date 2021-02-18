import Account_Info, config, Alpaca_Functions

api = Account_Info.getAccount()


def margingains(n_day, current_day):
    total = 0
    for i in n_day:
        total += float(i)
    moving_average = total / len(n_day)
    if current_day > moving_average * 1.05:
        return "sell"
    else:
        return "buy"


def calculateMR(stock_in, x=3, starting=1000):
    # x is for how many days average we want to do our MACD then is used to traverse through the data.
    # indicates the amount we want to start with
    daily_close_list = stock_in
    day_average = x
    # print(daily_close_list)# uncomment this line if you need to check the loader

    status = 0  # indicates whether we are in a sold or have our money or bought and we are invested

    account = starting  # sets up our account that will buy and sell from

    amount = 0  # sets up how much of the stock we own

    print('start account: ' + str(account))

    # counters for how many buys and sells have been made.
    buy_counter = 0
    sell_counter = 0
    while x < len(daily_close_list):

        # the next commented line is a messed up list but for some reason it works really well
        # day_list = [daily_close_list[x-i] for i in range(x-2, x)]

        day_list = [daily_close_list[i].c for i in range(x - day_average, x)]  # here is a proper MACD
        # print(day_list, daily_close_list[x].c)
        do_what = margingains(day_list, daily_close_list[x].c)

        # code for if the MACD algorithm outputed a buy
        if do_what == 'buy' and status == 0:
            # divides the price by the value we have to buy as much of the stock as possible.
            amount = account / daily_close_list[x].c
            account -= amount * daily_close_list[x].c
            print('buy at: ' + str(daily_close_list[x].c))
            print('account now at:' + str(account))
            buy_counter += 1
            status = 1

        # code for if the MACD algorithm outputed a sell
        elif do_what == 'sell' and status == 1:
            account += amount * daily_close_list[x].c
            print('sell stock at: ' + str(daily_close_list[x].c) )
            print('account now at:' + str(account))
            status = 0
            sell_counter += 1
        x += 1

    # sells based on last price so we can see the total.
    if status == 1:
        account += amount * daily_close_list[x - 1].c
        print('sell stock at: ' + str(daily_close_list[x - 1].c))
        print('account now at:' + str(account))
        sell_counter += 1

    # Print Statistics from the data.
    print('amount of buys: ' + str(buy_counter))
    print('amount of sells: ' + str(sell_counter))
    print('account at day ' + str(x) + ': ' + str(account))
    print('percent gain: ' + str((account / starting * 100) - 100) + "%" + '\n')



account = api.get_account()

print("MSFT")
bar_set = api.get_barset('MSFT', 'day', limit=250)
stock = bar_set['MSFT']
calculateMR(stock, 1, 1000)

print("AAPL")
bar_set = api.get_barset('AAPL', 'day', limit=250 )
stock = bar_set['AAPL']
calculateMR(stock, 1, 1000)

print("AMD")
bar_set = api.get_barset('AMD', 'day', limit=250 )
stock = bar_set['AMD']
calculateMR(stock, 1, 1000)

# print("RCL")
# bar_set = api.get_barset('RCL', 'day',)
# stock = bar_set['RCL']
# calculateMR(stock, 3, 1000)