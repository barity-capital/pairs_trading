from config_execution_api import *
from binance.client import Client
import datetime
import time

# Create a function to return position info by passing api_url


client = Client(api_key, api_secret)
# Get position info
def get_position_info(ticker):
    
    size = ""
    side = 0
    position_info = client.futures_position_information()
    for i in position_info:
        if i["symbol"] == ticker:
            # if ticker == ticker:
            if float(i["positionAmt"]) != 0:
                if float(i["notional"]) > 0: # This is "LONG" position
                    side = "LONG"
                    size = float(i["positionAmt"])
                elif float(i["notional"]) < 0: # This is "SHORT" position
                    # if ticker == ticker:
                    side = "SHORT"
                    size = float(i["positionAmt"])

            # print(i)
            # current_position = float(i["positionAmt"])
            # print(float(i["positionAmt"]))
    return (size, side)
pos_info = get_position_info("ZENUSDT")
print(pos_info)

time_start_date =0
if timeframe == "1h":
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == "1d":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)
time_start_seconds = int(time_start_date.timestamp())
# Place close market order
def place_market_close_order(ticker, side, size):
    if side[1] == "LONG":
        side_close = "SELL"
    elif side[1] == "SHORT":
        side_close = "BUY"
    

    # Close position
    client.futures_create_order(
        symbol=ticker,
        side=side_close,
        type="MARKET",
        quantity = abs(size[0])
    )
    return
place_market_close_order("ZENUSDT", pos_info, pos_info)