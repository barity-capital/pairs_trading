import websocket
import json
import ssl
import time

from config_execution_api import ticker_1, ticker_2, signal_positive_ticker, signal_negative_ticker
from config_execution_api import ticker_1, ws_public_url, ticker_2
from config_execution_api import api_key, api_secret
from func_execution_calls import place_order
from func_position_calls import open_order_confirmation, active_position_confirmation
from func_execution_calls import set_leverage
from func_save_status import save_status
from func_get_zscore import get_latest_zscore
from func_trade_management import manage_new_trade
from func_close_position import close_all_positions

def on_message(ws, message):
    global count
    global signal_side

    if count == 0:
        # Initial printout
        print("Initilizing...")

        # Initialize variables
        status_dict = {"message": "Start now!"}
        order_long = {}
        order_short = {}
        signal_sign_positive = False
        kill_switch = 0
        signal_side = ''


        # Set leverage in case forgotten to do so in platform
        print("Setting leverage...")
        set_leverage(signal_positive_ticker)
        set_leverage(signal_negative_ticker)

        # Comment bot
        print("Getting orderbook information...")
        data = json.loads(message)

        orderbook = data["data"]

        # current_zscore, signal_sign, zscore_list = get_latest_zscore(orderbook)
        # # print("Zscore Updated:", zscore_list)
        # print("Current zscore is not hot:", current_zscore)

        # Check if open trade already exists
        is_p_ticker_active = active_position_confirmation(orderbook)
        is_n_ticker_active = active_position_confirmation(orderbook)
        is_p_ticker_open = open_order_confirmation(orderbook)
        is_n_ticker_open = open_order_confirmation(orderbook)
        # print("done")
        
        check_all = [is_p_ticker_active, is_n_ticker_active, is_p_ticker_open, is_n_ticker_open]
        is_manage_new_trades = not all(check_all)
        # print(is_manage_new_trades)

        # Update status_dict with values of check_all
        if is_manage_new_trades and kill_switch == 0:
            current_zscore, signal_sign, zscore_list, current_spread = get_latest_zscore(orderbook)
            print("Anh thay em nay the nao?")
            print("Vong 1:", current_zscore, "Vong 2:", current_spread)
            status_dict["message"] = "Initial check made..."
            status_dict["checks"] = check_all
            save_status(status_dict)
            kill_switch, signal_side, enter_trade_zscore, enter_trade_spread = manage_new_trade(orderbook, kill_switch)
            # print("")
            
            # return kill_switch
            # print("Current zscore: ", current_zscore, "Enter zscore: ", enter_trade_zscore)
        
            # print(kill_switch)

        # Managing open kill switch
    # if count == 1:    
        while kill_switch == 1:
            updated_zscore, signal_sign, zscore_list, updated_spread = get_latest_zscore(orderbook)

            print("Current zscore: ", updated_zscore, "Enter zscore: ", enter_trade_zscore, "Current spread: ", updated_spread, "Enter spread:", enter_trade_spread)

            time.sleep(1)
            # Close positions
            if signal_side == "positive" and updated_spread < 0:
                kill_switch = 2
                # count += 1
            if signal_side == "negative" and updated_spread > 0:
                kill_switch = 2
                # count += 1
            # Put back to zero if trades are closed
            # if is_manage_new_trades and kill_switch != 2:
            #     kill_switch = 0

        # Close all active orders and positions
        if kill_switch == 2:
            status_dict["message"] = "Tao ban do ton kho..."
            kill_switch = close_all_positions(kill_switch)

          # Increment count to indicate that the order has been placed
    # count += 1
    # # Check for signal side change
    # while True:
    #     if signal_side == "positive" or signal_side == "negative":
    #         break
    #     time.sleep(1)

    # # Continue with further actions based on signal_side
    # if signal_side == "positive":
    #     # Perform actions when signal_side changes to positive
    #     pass
    # elif signal_side == "negative":
    #     # Perform actions when signal_side changes to negative
    #     pass

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
count = 0

# while True:
        # Connect to the WebSocket streams for each ticker
try:

    stream_url = f"{ws_public_url}/stream?streams={ticker_1}@depth{levels}/{ticker_2}@depth{levels}"
    
    # Connect to WebSocket with SSL certificate verification disabled
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(stream_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Continuously receive messages from the WebSocket connection
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

except Exception as e:
    print("Error:", e)