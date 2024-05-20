from binance.client import Client
from config_execution_api import *
from func_close_position import *
from func_calculation import *

# Set leverage
client = Client(api_key, api_secret)

def set_leverage(ticker):
    try:
        leverage = 1
        client.futures_change_leverage(symbol=ticker, leverage=leverage)
    except Exception as e:
        pass
    return

# Function to adjust order quantity to meet minimum notional value
# def adjust_order_quantity(ticker, price, quantity):
#     notional_value = float(price) * float(quantity)
#     if notional_value < 5:
#         adjusted_quantity = 5 / float(price)
#         print("Adjusted order quantity for", ticker, ":", adjusted_quantity)
#         return adjusted_quantity
#     return quantity

# Place limit or market order
def place_order(ticker, price, initial_capital_usdt, direction):
    # Set order side
    if direction == "Long":
        side = "BUY"
    else:
        side = "SELL"
    
    # Determine order type
    if limit_order_basis:
        type_order = "LIMIT"


        order = client.futures_create_order(
        symbol=ticker,
        side=side,
        type=type_order,
        price=price,
        quantity=initial_capital_usdt,
        reduceOnly=False,
        timeinforce="GTC",
        closePosition=False
    )
    else:
        type_order = "MARKET"

        order = client.futures_create_order(
            symbol=ticker,
            side=side,
            type=type_order,
            # price=price,
            quantity=initial_capital_usdt,
            reduceOnly=False,
            # timeinforce="GTC",
            closePosition=False
        )

    # Adjust order quantity if needed
    # adjusted_quantity = adjust_order_quantity(ticker, price, initial_capital_usdt)

    # Place the order

    if order:
        order_id = order["orderId"]
    else:
        order_id = None
    
    return order_id

# Initialize execution
