from config_execution_api import *
# import datetime
# import time
# import requests
import time
# import hashlib
# import hmac
# import urllib.parse

# Create a function to return position info by passing api_url


# Get position info
def get_position_info(ticker):
    
    size = ""
    side = 0
    position_info = client.futures_position_information()

    # Get open orders from clien

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
# pos_info = get_position_info("")
# print(pos_info)

# time_start_date =0
# if timeframe == "1h":
#     time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
# if timeframe == "1d":
#     time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)
# time_start_seconds = int(time_start_date.timestamp())
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

# # Close all positions for both ticker
def close_all_positions(kill_switch):


    # # Cancel all active order
    client.futures_cancel_all_open_orders(symbol = signal_positive_ticker)
    client.futures_cancel_all_open_orders(symbol = signal_negative_ticker)
    
    # Get position info
    pos_infor_positive = get_position_info(ticker = signal_positive_ticker)
    pos_infor_negative = get_position_info(ticker = signal_negative_ticker)

    # # # Get position info
    # # side_1 = get_position_info(signal_positive_ticker)[1]
    # # size_1 = get_position_info(signal_positive_ticker)[0]

    # # side_2 = get_position_info(signal_negative_ticker)[1]
    # # size_2 = get_position_info(signal_negative_ticker)[0]

    # # Close position
    place_market_close_order(signal_positive_ticker, pos_infor_positive, pos_infor_positive)
    place_market_close_order(signal_negative_ticker, pos_infor_negative, pos_infor_negative)
    kill_switch = 0
    return kill_switch

# close_all_positions()