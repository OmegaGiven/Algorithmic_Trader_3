from coinbase.wallet.client import Client
import config

api_key = config.api_key
api_secret = config.api_secret
api_version = config.api_version

client = Client(api_key,
                api_secret,
                api_version=api_version)

payment_methods = client.get_payment_methods()




account = client.get_primary_account()
payment_method = client.get_payment_methods()[0]

print(account)

# buy_price_threshold  = 200
# sell_price_threshold = 500
#
# buy_price  = client.get_buy_price(currency='USD')
# sell_price = client.get_sell_price(currency='USD')
#
# if float(sell_price.amount) <= sell_price_threshold:
#   sell = account.sell(amount='1',
#                       currency="BTC",
#                       payment_method=payment_method.id)
#
#
# if float(buy_price.amount) <= buy_price_threshold:
#   buy = account.buy(amount='1',
#                     currency="BTC",
#                     payment_method=payment_method.id)