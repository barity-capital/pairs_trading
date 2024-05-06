from config_execution_api import client

# def get_top_5_orders(ticker):
#     client.fu(symbol=ticker, limit=5)
#     return liquidity, last_price
def get_avtive_positions(ticker): # ticker, direction = "Long"

    # Get position
    position = client.futures_position_information(symbol = ticker)

    print(position)

get_avtive_positions("ZENUSDT")

"""
1 BTC = 60k USDT
---
x BTC = 50 USDT
"""