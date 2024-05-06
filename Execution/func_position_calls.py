# from binance.client import Client
from config_execution_api import client
from func_prices_call import get_timestamps
from config_execution_api import ticker_1, ticker_2, signal_negative_ticker, signal_positive_ticker


"""
Order status (status):

NEW
PARTIALLY_FILLED
FILLED
CANCELED
REJECTED
EXPIRED
EXPIRED_IN_MATCH
"""

# Check for open positions
def active_position_confirmation(orderbook):
    try:
        data_for_position = client.futures_position_information()
        for i in orderbook:
            if orderbook["s"] == signal_positive_ticker:
                for i in data_for_position:
                    if float(i["positionAmt"]) != 0:
                            return True
            elif orderbook["s"] == signal_negative_ticker:
                for i in data_for_position:
                    if float(i["positionAmt"]) != 0:
                            return True
    except:
        return False
    return False

# Check for open positions
def open_order_confirmation(orderbook):
    try:
        data_for_order = client.futures_get_all_orders()
        for i in orderbook:
            if orderbook["s"] == signal_positive_ticker:
                # print(position)
                for i in data_for_order:
                    if i["status"] == "NEW" or i["status"] == "PARTIALLY_FILLED":
                        return True
            elif orderbook["s"] == signal_negative_ticker:
                # print(position)
                for i in data_for_order:
                    if i["status"] == "NEW" or i["status"] == "PARTIALLY_FILLED":
                        return True
        #     if float(i["positionAmt"]) != 0:
        #         return True

    except:
        return True

    return False

def get_open_orders(): # ticker, direction = "Long"

    # Get position
    position = client.futures_get_all_orders()

    # Get current open order status
    for i in position:
        if i["status"] == "NEW" or i["status"] == "PARTIALLY_FILLED":
            # Change order status
            order_id = i["orderId"]
            order_status = i["status"]
            original_quantity = abs(float(i["origQty"]))
            order_price = i["price"]
    return order_price, original_quantity, order_id, order_status

def get_avtive_positions(ticker): # ticker, direction = "Long"

    # Get position
    position = client.futures_position_information(symbol = ticker)

    # Get current open order status
    position_price = float(position[0]["markPrice"])
    position_quantity = abs(float(position[0]["positionAmt"]))
    
    # print(position_price, position_quantity)
    return position_price, position_quantity




# get_open_position()
# open_position_confirmation("ETHUSDT")