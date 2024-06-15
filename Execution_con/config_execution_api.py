"""
    API Docs
    https://binance-docs.github.io/apidocs/futures/en/#change-log
    wss://testnet.binancefuture.com/ws-fapi/v1
    The REST baseurl for testnet is "https://testnet.binancefuture.com"
    The Websocket baseurl for testnet is "wss://fstream.binancefuture.com"
    Example:
    wss://fstream.binance.com/ws/bnbusdt@aggTrade
    wss://fstream.binance.com/stream?streams=bnbusdt@aggTrade/btcusdt@markPrice
"""
from binance.client import Client


# Config variables
mode = "on"
ticker_1 = "OCEANUSDT"
ticker_2 = "AGIXUSDT"  # OCEANUSDT
signal_positive_ticker = ticker_1
signal_negative_ticker = ticker_2
rounding_ticker_1 = 2
rounding_ticker_2 = 2
quantity_rounding_ticker_1 = 0
quantity_rounding_ticker_2 = 3

# Will ensure positions (expect for close) will be placed on limit basis
limit_order_basis = False

# Total tradeable capital to be split between both pairs # Test lower liquidity
tradeable_capital_usdt = 50
stop_loss_fail_safe = 0.15  # Stop loss at market order in case of drastic event
signal_trigger_thresh = 0  # Z-score threshold to trigger signal (must above 0)

timeframe = "1h"  # make sure matches your strategy timeframe
kline_limit = 500  # make sure matches your strategy timeframe
z_score_window = 21  # make sure matches your strategy timeframe

# Live API
api_key_mainnet = "X5YOXEAJAvbsy57O0RG9y1LZTtfJpHKtBSZu05iDDF1biOryTqp0RXHkIMuXZgcE"
api_secret_mainnet = "qc6ets7DqAROveLD2YYN3RUtOBZDsOQjNNzJOxxqWE4F0pzGYYl7ky2x7KbVkH00"

# Test API
api_key_testnet = ""
api_secret_testnet = ""

# Selected API
api_key = api_key_testnet if mode == "test" else api_key_mainnet
api_secret = api_secret_testnet if mode == "test" else api_secret_mainnet

# Selected URL
api_url = "https://testnet.binancefuture.com" if mode == "test" else "https://fapi.binance.com"
ws_public_url = "wss://testnet.binance.vision/ws-api" if mode == "test" else "wss://fstream.binance.com/ws"

# Client
client = Client(api_key, api_secret)
