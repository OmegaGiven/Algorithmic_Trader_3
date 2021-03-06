import csv

def loader(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        daily_close = []
        daily_close_dates = []
        for row in csv_reader:
            if line_count != 0:
                daily_close.append(float(row[4]))
                daily_close_dates.append(row[0])
            line_count += 1
        # print(f'Processed {line_count} lines.')
        return daily_close, daily_close_dates


# Our MACD function takes a set of days and calculates the average.
def macd(n_day, current_day):
    total = 0
    for i in n_day:
        total += float(i)
    moving_average = total / len(n_day)

    # takes a percent of the average, if less than the current day we buy
    if current_day > moving_average * 0.95:
        return 'buy'
    else:
        return 'sell'


# Margingains is the reverse of MACD if you wanted to try that just replace the funciton in calculate
def margingains(n_day, current_day):
    total = 0
    for i in n_day:
        total += float(i)
    moving_average = total / len(n_day)
    if current_day > moving_average * 1.05:
        return "sell"
    else:
        return "buy"


def calculateMACD(filename, x=3, starting=1000):
    daily_close_list, daily_close_dates = loader(filename)
    # starting indicates the amount we want to start with
    # x is for how many days average we want to do our MACD then is used to traverse through the data.
    # print(daily_close_list)# uncomment this line if you need to check the loader
    day_average = x+1
    status = 0  # indicates whether we are in a sold or have our money or bought and we are invested

    starting = 100000

    account = starting  # sets up our account that will buy and sell from

    amount = 0  # sets up how much of the stock we own

    print('start account: ' + str(account))

    # counters for how many buys and sells have been made.
    buy_counter = 0
    sell_counter = 0
    while x < len(daily_close_list):

        # the next commented line is a messed up list but for some reason it works really well
        # day_list = [daily_close_list[x-i] for i in range(x-2, x)]

        day_list = [daily_close_list[i] for i in range(x - day_average, x)] # here is a proper MACD

        do_what = macd(day_list, daily_close_list[x])

        # code for if the MACD algorithm outputed a buy
        if do_what == 'buy' and status == 0:
            # divides the price by the value we have to buy as much of the stock as possible.
            amount = account / daily_close_list[x]
            account -= amount * daily_close_list[x]
            print('buy at: ' + str(daily_close_list[x]) + ' on: ' + daily_close_dates[x])
            print('account now at:' + str(account))
            buy_counter += 1
            status = 1

        # code for if the MACD algorithm outputed a sell
        elif do_what == 'sell' and status == 1:
            account += amount * daily_close_list[x]
            print('sell stock at: ' + str(daily_close_list[x]) + ' on: ' + daily_close_dates[x])
            print('account now at:' + str(account))
            status = 0
            sell_counter += 1
        x += 1

    # sells based on last price so we can see the total.
    if status == 1:
        account += amount * daily_close_list[x-1]
        print('sell stock at: ' + str(daily_close_list[x - 1]) + ' on: ' + daily_close_dates[x-1])
        print('account now at:' + str(account))
        sell_counter += 1

    # Print Statistics from the data.
    print('amount of buys: ' + str(buy_counter))
    print('amount of sells: ' + str(sell_counter))
    print('account at day ' + str(x) + ': ' + str(account))
    print('percent gain: ' + str((account / starting * 100) - 100) + "%" + '\n')


def calculateMR(filename, x=3, starting=1000):
    # x is for how many days average we want to do our MACD then is used to traverse through the data.
    # indicates the amount we want to start with
    daily_close_list, daily_close_dates = loader(filename)
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

        day_list = [daily_close_list[i] for i in range(x - day_average, x)] # here is a proper MACD
        do_what = margingains(day_list, daily_close_list[x])

        # code for if the MACD algorithm outputed a buy
        if do_what == 'buy' and status == 0:
            # divides the price by the value we have to buy as much of the stock as possible.
            amount = account / daily_close_list[x]
            account -= amount * daily_close_list[x]
            print('buy at: ' + str(daily_close_list[x]) + ' on: ' + daily_close_dates[x])
            print('account now at:' + str(account))
            buy_counter += 1
            status = 1

        # code for if the MACD algorithm outputed a sell
        elif do_what == 'sell' and status == 1:
            account += amount * daily_close_list[x]
            print('sell stock at: ' + str(daily_close_list[x]) + ' on: ' + daily_close_dates[x])
            print('account now at:' + str(account))
            status = 0
            sell_counter += 1
        x += 1

    # sells based on last price so we can see the total.
    if status == 1:
        account += amount * daily_close_list[x-1]
        print('sell stock at: ' + str(daily_close_list[x - 1]) + ' on: ' + daily_close_dates[x-1])
        print('account now at:' + str(account))
        sell_counter += 1

    # Print Statistics from the data.
    print('amount of buys: ' + str(buy_counter))
    print('amount of sells: ' + str(sell_counter))
    print('account at day ' + str(x) + ': ' + str(account))
    print('percent gain: ' + str((account / starting * 100) - 100) + "%" + '\n')
