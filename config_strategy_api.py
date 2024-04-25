"""
    API Docs
    https://binance-docs.github.io/apidocs/futures/en/#change-log
    wss://testnet.binancefuture.com/ws-fapi/v1
    The REST baseurl for testnet is "https://testnet.binancefuture.com"
    The Websocket baseurl for testnet is "wss://fstream.binancefuture.com"
"""

# API imports
# from binance.cm_futures import CMFutures
import asyncio
# import websockets
import ssl
# from func_prices_klines import time_start_seconds




# CONFIG
mode = "test"
timeframe = "1h"
kline_limit = 500
z_score_window = 21

# Live API
api_key_mainnet = "X5YOXEAJAvbsy57O0RG9y1LZTtfJpHKtBSZu05iDDF1biOryTqp0RXHkIMuXZgcE"
api_secret_mainnet = "qc6ets7DqAROveLD2YYN3RUtOBZDsOQjNNzJOxxqWE4F0pzGYYl7ky2x7KbVkH00"

# Test API
api_key_testnet = "3be0890bbc63069ba82db571246f2e89ef1e69ee85bab7bf1792df6e3d74b819"
api_secret_testnet = "2c0180a9a5d9dcbb6e4e043f97d99bfe4b47735ddad684f359d64fc9c63296da"

# Selected API
api_key = api_key_testnet if mode == "test" else api_key_mainnet
api_secret = api_secret_testnet if mode == "test" else api_secret_mainnet

# Selected URL
api_url = "https://testnet.binancefuture.com" if mode == "test" else "https://fapi.binance.com"

# define a function to get information for btcusdt from /fapi/v1/exchangeInfo
import requests

# HTTP request
def get_ticker_info(ticker):
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        exchange_info = response.json()
        symbols = exchange_info.get('symbols', [])
        for symbol in symbols:
            if symbol['symbol'] == f'{ticker}':
                return symbol
        return None
    else:
        print("Failed to fetch exchange information:", response.text)
        return None


def get_spot_exchange_info():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        exchange_info = response.json()
        return exchange_info
    else:
        print("Failed to fetch exchange information:", response.text)
        return None

# Get historical prices (klines)
def query_mark_price_kline(symbol, interval):
    url = "https://fapi.binance.com/fapi/v1/markPriceKlines"
    params = {
        "symbol": symbol,
        "interval": interval,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        klines = response.json()
        return klines  # Print the klines
    else:
        print("Failed to fetch klines:", response.text)
        return None

    # print(klines)

# query_mark_price_kline("BTCUSDT", "1h")

#     # Get prices
    # return mark_price




# # Websoccket Connection
# async def connect_websocket(symbol):
#         ssl_context = ssl.create_default_context()
#         ssl_context.check_hostname = False
#         ssl_context.verify_mode = ssl.CERT_NONE

#         uri = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"  # WebSocket URL for Binance ticker stream

#         async with websockets.connect(uri, ssl=ssl_context) as websocket:
#             while True:
#                 response = await websocket.recv()
#                 print(response)

# asyncio.get_event_loop().run_until_complete(connect_websocket())