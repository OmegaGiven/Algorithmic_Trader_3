from os import listdir
import MACD
import YahooHistoryDownloader

"""
Put the name of the stock you want to check for example:
["DOGE-USD","MSFT", "TSLA", "AMD", "IIPR"] and 
this will download the data and run the MACD on it
"""
# Negative companies "IBM", "BTI", "MO", "INTC"
# "DOGE-USD", "TSLA", "AMD", "IIPR", "NVDA", "BTC-USD",
ticer_List = ["MSFT", "AMD", "AAPL", "TMUS"]
YahooHistoryDownloader.download(ticer_List)

testFiles = listdir("./testFiles")
for x in testFiles:
    print("testing: " + x)
    print('MACD:')
    MACD.calculateMACD("testFiles/" + x)
    print('Mean Revision:')
    MACD.calculateMR("testFiles/" + x)
    print('\n\n\n')

input("Press Enter to Quit")
