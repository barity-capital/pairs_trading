"""
    interval: 1h
    from: integer from timestamp in seconds
    limit: max size of 200
"""

from config_strategy_api import *
import datetime
import time

# Get start times
time_start_date =0
if timeframe == "1h":
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == "1d":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)
time_start_seconds = int(time_start_date.timestamp())
print(time_start_seconds)


# Get historical prices (klines)
# def get_prices_klines(symbol,timeframe):

# # #     # Get prices
#     kline_info = query_mark_price_kline(symbol=symbol, interval=timeframe)
#     for i in kline_info:
#         # print(i)
#         return i[4]

         
# get_prices_klines("BTCUSDT", "1h")