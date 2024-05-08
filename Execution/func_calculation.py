import math
from config_execution_api import *
import requests
from func_position_calls import active_position_confirmation

# Function to get price and quantity precision for a given trading pair
def get_precision(symbol):
    exchange_info_url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(exchange_info_url)
    exchange_info = response.json()
    for symbol_info in exchange_info["symbols"]:
        if symbol_info["symbol"] == symbol:
            price_precision = symbol_info["pricePrecision"]
            quantity_precision = symbol_info["quantityPrecision"]
            return price_precision, quantity_precision
    return None, None  # Return None if symbol is not found

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
def get_trade_details(orderbook, direction ="Long", capital = 50):
    
    # for i in orderbook["b"]:
    #     print(i)
    # Set calculation and output variables
    # price_rounding = 20
    # quantity_rounding = 20
    mid_price = 0
    quantity = 0
    stop_loss = 0
    bid_prices_list = []
    ask_prices_list = []
    bid_quantity_list = []
    ask_quantity_list = []

    # Get prices, stop loss quantity
    if orderbook:

        # Set price rounding
        # price_rounding = rounding_ticker_1 if orderbook["s"] == ticker_1 else rounding_ticker_2
        # quantity_rounding = quantity_rounding_ticker_1 if orderbook["s"] == ticker_1 else quantity_rounding_ticker_2

        
        # Organize prices
        for i in orderbook["b"]: # and 
            # check_active_order_result = active_position_confirmation(ticker)
            bid_prices_list.append(float(i[0]))
            bid_quantity_list.append(float(i[1]))
        for j in orderbook["a"]:
            ask_prices_list.append(float(j[0]))
            ask_quantity_list.append(float(j[1]))
        ask_prices_list.reverse()
        # print(bid_items_list, ask_items_list)
        # # Calculate price, size , stoploss and average liquidity
        # if len(ask_items_list) > 0 and len(bid_items_list) > 0:

            # Get nearest ask, nearest bid and orderbook spread
        nearest_ask = ask_prices_list[0]
        top_5_amount_ask = sum(ask_quantity_list[:5])
        nearest_bid = bid_prices_list[0]
        top_5_amount_bid = sum(bid_quantity_list[:5])

        # Calculate mid price
        if direction == "Long":
            mid_price = nearest_bid # Placing at bid has higher chance of not being cancelled
            quantity = top_5_amount_bid
        else:
            mid_price = nearest_ask # Placing at bid has higher chance of not being cancelled
            quantity = top_5_amount_ask
        # stop_loss = round(mid_price - (mid_price * stop_loss_fail_safe), price_rounding)

        # # Calculate quantity
        # quantity = capital / mid_price
        
        # mid_price = round(mid_price, )
        if orderbook["s"] == ticker_1.upper() or orderbook["s"] == ticker_2.upper():
            price_precision, quantity_precision = get_precision(orderbook["s"])
            if price_precision is not None or quantity_precision is not None:
            # Round price and quantity according to precision
                rounded_price = round(mid_price, price_precision)
                rounded_quantity = round(quantity, quantity_precision)
             # Mid price and quantity must have same precision to pass in client.futures_create_order
        # mid_price = round(mid_price, price_rounding - 1)
        # quantity = round(quantity, quantity_rounding - 1)


    # Output result
    # print(f"Mid price: {mid_price}, Quantity: {quantity}")
    # fix mid and quantity to have same precision
    time.sleep(5)
    return rounded_price, rounded_quantity


