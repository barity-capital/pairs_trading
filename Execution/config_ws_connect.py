import websocket
import json
from config_execution_api import ticker_1, ws_public_url, ticker_2
from func_calculation import get_trade_details
import time
# Define your WebSocket event handlers here
def on_message(ws, message):

    data = json.loads(message)
    unpacked_data = data["data"]
        
        
    # print(data)
    # for i in data:
    #     print(i)
    trade_details = get_trade_details(unpacked_data, direction ="Long", capital = 1000)
    # trade_details[0]
    print(trade_details)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")

# Define your ticker symbols and other variables
levels = 5
ticker_1 = ticker_1.lower()
ticker_2 = ticker_2.lower()
ws_public_url = "wss://fstream.binance.com"
tickers = [ticker_1, ticker_2]

# Connect to the WebSocket streams for each ticker
start_time = time.time()
while True:
    for ticker in tickers:
        stream_url = f"{ws_public_url}/stream?streams={ticker_1}@depth{levels}/{ticker_2}@depth{levels}"

        # Connect to WebSocket
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(stream_url,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        # Close after running for 5 minutes
        print("hellp")
        ws.run_forever()

    time.sleep(5)





# import websocket
# import json
# from config_execution_api import ticker_1, ws_public_url, ticker_2, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2
# import time
# from func_calculation import get_trade_details
# def on_message(ws, message):
#     data = json.loads(message)
#     print(data)

# def on_error(ws, error):
#     print(error)

# def on_close(ws):
#     print("### closed ###")

# def on_open(ws):
#     print("### connected ###")


# levels = 5
# # Convert ticker_1 to lower case
# ticker_1 = ticker_1.lower()
# ticker_2 = ticker_2.lower()
# while True:
#     for ticker in [ticker_1, ticker_2]:
#         stream_url = f"{ws_public_url}/{ticker}@depth{levels}"

#         websocket.enableTrace(True)
#         ws = websocket.WebSocketApp(stream_url,
#                                     on_message=on_message,
#                                     on_error=on_error,
#                                     on_close=on_close)
#         ws.on_open = on_open
#         ws.run_forever()

#         # access to websocket object and make a variable to contain "s"
#         ws["s"] = ticker
#         # get_trade_details(ws, direction ="Long", capital = 0)
#         # if ticker_1.upper() == ws["s"]:
#         #     price_rounding = rounding_ticker_1
#         # else:
#         #     rounding_ticker_2
#         # quantity_rounding = quantity_rounding_ticker_1 if ticker_1.upper() == ws["s"] else quantity_rounding_ticker_2


#         # for data in ws:
#         #     print(data["s"])
#     # Wait for some time before fetching data for the next symbol
#     time.sleep(10)  # Adjust the sleep duration as needed