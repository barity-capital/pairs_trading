from config_execution_api import client

# def get_top_5_orders(ticker):
#     client.fu(symbol=ticker, limit=5)
#     return liquidity, last_price

requests = client.get_account()
print(requests)

"""
1 BTC = 60k USDT
---
x BTC = 50 USDT
"""