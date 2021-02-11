from os import listdir
import MACD
import YahooHistoryDownloader

"""
Put the name of the stock you want to check for example:
["DOGE-USD","MSFT", "TSLA", "AMD", "IIPR"] and 
this will download the data and run the MACD on it
"""

ticer_List = ["DOGE-USD","MSFT", "TSLA", "AMD", "IIPR", "NVDA", "BTC-USD", "IBM", "BTI", "MO", "INTC"]
YahooHistoryDownloader.download(ticer_List)

testFiles = listdir("./testFiles")
for x in testFiles:
    print("testing: " + x)
    MACD.calculate("testFiles/" + x)

input("Press Enter to Quit")
