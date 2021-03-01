import config, Alpaca_Functions
import csv

api = Alpaca_Functions.getAccount()
macd105 = "macd105"
macd100 = "macd100"
macd095 = "macd095"
mr095 = "mr095"
mr100 = "mr100"
mr105 = "mr105"


def decision_method(n_day, current_day, operation=macd105):
    total = 0
    for i in n_day:
        total += float(i)
    moving_average = total / len(n_day)

    if operation == macd105:
        if current_day > moving_average * 1.05:
            return "sell"
        else:
            return "buy"
    if operation == macd100:
        if current_day > moving_average:
            return "sell"
        else:
            return "buy"
    if operation == macd095:
        if current_day > moving_average * 0.95:
            return "sell"
        else:
            return "buy"
    if operation == mr095:
        if current_day < moving_average * 0.95:
            return "sell"
        else:
            return "buy"
    if operation == mr100:
        if current_day < moving_average:
            return "sell"
        else:
            return "buy"
    if operation == mr105:
        if current_day < moving_average * 1.05:
            return "sell"
        else:
            return "buy"


def calculate(stock_in, x=3, starting=1000, method=macd105):
    # x is for how many days average we want to do our MACD then is used to traverse through the data.
    # indicates the amount we want to start with
    daily_close_list = stock_in
    day_average = x
    # print(daily_close_list)# uncomment this line if you need to check the loader

    status = 0  # indicates whether we are in a sold or have our money or bought and we are invested

    account = starting  # sets up our account that will buy and sell from

    amount = 0  # sets up how much of the stock we own

    account_over_time = []
    buy_over_time = []
    sell_over_time = []
    print('start account: ' + str(account))

    # counters for how many buys and sells have been made.
    buy_counter = 0
    sell_counter = 0
    print(daily_close_list)
    while x < len(daily_close_list):

        # the next commented line is a messed up list but for some reason it works really well
        # day_list = [daily_close_list[x-i] for i in range(x-2, x)]

        day_list = [daily_close_list[i].c for i in range(x - day_average, x)]  # here is a proper MACD
        # print(day_list, daily_close_list[x].c)
        do_what = decision_method(day_list, daily_close_list[x].c, method)
        print(day_list)
        # code for if the MACD algorithm outputed a buy
        if do_what == 'buy' and status == 0:
            # divides the price by the value we have to buy as much of the stock as possible.
            amount = account / daily_close_list[x].c
            account -= amount * daily_close_list[x].c
            buy_over_time.append(daily_close_list[x].c)
            account_over_time.append(account)
            buy_counter += 1
            status = 1

        # code for if the MACD algorithm outputed a sell
        elif do_what == 'sell' and status == 1:
            account += amount * daily_close_list[x].c
            sell_over_time.append(daily_close_list[x].c)
            account_over_time.append(account)
            status = 0
            sell_counter += 1
        x += 1

    # sells based on last price so we can see the total.
    if status == 1:
        account += amount * daily_close_list[x - 1].c
        sell_over_time.append(daily_close_list[x-1].c)
        account_over_time.append(account)
        sell_counter += 1

    # Print Statistics from the data.
    print('amount of buys: ' + str(buy_counter))
    print('amount of sells: ' + str(sell_counter))
    print('account at day ' + str(x) + ': ' + str(account))
    percent_gain = [(account / starting * 100) - 100]
    print('percent gain: ' + str(percent_gain[0]) + "%" + '\n')
    return account_over_time, buy_over_time, sell_over_time, percent_gain


account = api.get_account()
stocks = ["RCL"]
with open('historicalTest.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for x in stocks:
        print(x)
        bar_set = api.get_barset(x, 'day', limit=7)
        stock = bar_set[x]

        account_over_time, buy_over_time, sell_over_time, percent_gain = calculate(stock, 1, 1000)
        writer.writerow([x, macd105])
        writer.writerow(account_over_time)
        writer.writerow(buy_over_time)
        writer.writerow(sell_over_time)
        writer.writerow(percent_gain)
        writer.writerow([])

        account_over_time, buy_over_time, sell_over_time, percent_gain = calculate(stock, 1, 1000, macd100)
        writer.writerow([x, macd100])
        writer.writerow(account_over_time)
        writer.writerow(buy_over_time)
        writer.writerow(sell_over_time)
        writer.writerow(percent_gain)
        writer.writerow([])

        account_over_time, buy_over_time, sell_over_time, percent_gain = calculate(stock, 1, 1000, macd095)
        writer.writerow([x, macd095])
        writer.writerow(account_over_time)
        writer.writerow(buy_over_time)
        writer.writerow(sell_over_time)
        writer.writerow(percent_gain)
        writer.writerow([])

        account_over_time, buy_over_time, sell_over_time, percent_gain = calculate(stock, 3, 1000, mr095)
        writer.writerow([x, mr095])
        writer.writerow(account_over_time)
        writer.writerow(buy_over_time)
        writer.writerow(sell_over_time)
        writer.writerow(percent_gain)
        writer.writerow([])

        account_over_time, buy_over_time, sell_over_time, percent_gain = calculate(stock, 3, 1000, mr100)
        writer.writerow([x, mr100])
        writer.writerow(account_over_time)
        writer.writerow(buy_over_time)
        writer.writerow(sell_over_time)
        writer.writerow(percent_gain)
        writer.writerow([])

        account_over_time, buy_over_time, sell_over_time, percent_gain = calculate(stock, 3, 1000, mr105)
        writer.writerow([x, mr105])
        writer.writerow(account_over_time)
        writer.writerow(buy_over_time)
        writer.writerow(sell_over_time)
        writer.writerow(percent_gain)
        writer.writerow([])
