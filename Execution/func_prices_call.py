import datetime
from config_execution_api import *
# from config_ws_connect import *
import time


# Get start times
def get_timestamps():
    time_start_data = 0
    time_next_data = 0
    now = datetime.datetime.now()
    if timeframe == "1h":
        time_start_data = now - datetime.timedelta(hours=kline_limit)
        time_next_data = now + datetime.timedelta(hours=kline_limit)
    if timeframe == "1d":
        time_start_data = now - datetime.timedelta(days=kline_limit)
        time_next_data = now + datetime.timedelta(days=kline_limit)
    time_start_seconds = int(time_start_data.timestamp())
    time_next_seconds = int(time_next_data.timestamp())
    time_now_seconds = int(now.timestamp())
    # print( time_start_seconds, time_next_seconds, time_now_seconds)
    return time_start_seconds, time_next_seconds, time_now_seconds

# get_timestamps()

# Get total amount of first 5 orderbook
def get_price_klines():
    series_1 = []
    series_2 = []
    # time_start_seconds = get_timestamps()[0]
    prices_1 = client.futures_klines(symbol=ticker_1, interval=timeframe)
    # print(prices_1)
    prices_2 = client.futures_klines(symbol=ticker_2, interval=timeframe)
    if len(prices_1) > 0 and len(prices_2) > 0:
        for i in prices_1:
            series_1.append(float(i[4]))
        else:
            for i in prices_2:
                series_2.append(float(i[4]))
                                       

        
    # Manage API calls
    time.sleep(5)

    # Return prices output
    # print(series_1, series_2)
    return series_1, series_2


# get_price_klines()