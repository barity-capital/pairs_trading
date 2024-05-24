from config_execution_api import client

# def get_top_5_orders(ticker):
#     client.fu(symbol=ticker, limit=5)
#     return liquidity, last_price

requests = client.futures_klines("oceanusdt", "1h")
print(requests)

