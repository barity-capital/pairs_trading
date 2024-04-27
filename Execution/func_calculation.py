import math
from config_execution_api import *


# total_info = on_message()
def extract_close_prices(prices):
    # pass
    close_prices = []
    
    # print(price_data)
    for i in prices:
        if math.isnan(i):
            return []
        # append only same length i to close price

        close_prices.append(i)
    # print(close_prices)
    return close_prices

# Get trade details and latest prices
def get_trade_details(orderbook, direction ="Long", capital = 0):
    
    # for i in orderbook["b"]:
    #     print(i)
    # Set calculation and output variables
    price_rounding = 20
    quantity_rounding = 20
    mid_price = 0
    quantity = 0
    stop_loss = 0
    bid_items_list = []
    ask_items_list = []

    # Get prices, stop loss quantity
    if orderbook:

        # Set price rounding
        price_rounding = rounding_ticker_1 if orderbook["s"] == ticker_1 else rounding_ticker_2
        quantity_rounding = quantity_rounding_ticker_1 if orderbook["s"] == ticker_1 else quantity_rounding_ticker_2

        # Organize prices
        for i in orderbook["b"]:
            bid_items_list.append(float(i[0]))
        for j in orderbook["a"]:
            ask_items_list.append(float(j[0]))
        ask_items_list.reverse()
        # print(bid_items_list, ask_items_list)
        # # Calculate price, size , stoploss and average liquidity
        # if len(ask_items_list) > 0 and len(bid_items_list) > 0:

            # Get nearest ask, nearest bid and orderbook spread
        nearest_ask = ask_items_list[0]
        nearest_bid = bid_items_list[0]

        # Calculate mid price
        if direction == "Long":
            mid_price = nearest_bid # Placing at bid has higher chance of not being cancelled
        else:
            mid_price = nearest_ask # Placing at bid has higher chance of not being cancelled
        # stop_loss = round(mid_price - (mid_price * stop_loss_fail_safe), price_rounding)

        # Calculate quantity
        quantity = round(capital / mid_price, quantity_rounding)

    # Output result
    return (mid_price, quantity)


