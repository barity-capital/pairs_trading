from config_execution_api import signal_negative_ticker
from config_execution_api import signal_positive_ticker
from config_execution_api import signal_trigger_thresh
from config_execution_api import tradeable_capital_usdt
from config_execution_api import limit_order_basis
from config_execution_api import client
from func_get_zscore import get_latest_zscore
from func_calculation import get_trade_details
# from config_execution_api import client
from func_execution_calls import place_order
from func_calculation import get_precision
from func_order_review import check_order
import time

# def get_top_5_orders(ticker):
#     client.fu(symbol=ticker, limit=5)
#     return liquidity, last_price
def usdt_to_crypto_quantity(usdt_quantity, crypto_ticker):
    # Get the current price of the specified cryptocurrency against USDT
    ticker_info = client.get_symbol_ticker(symbol=crypto_ticker)
    if ticker_info:
        crypto_price = float(ticker_info['price'])
        # Convert the USDT quantity to the equivalent quantity of the cryptocurrency
        crypto_quantity = usdt_quantity / crypto_price
        return crypto_quantity
    else:
        print("Failed to retrieve ticker information.")
        return None


def get_liquidity(ticker):
    liquidity = client.futures_order_book(symbol=ticker)
    lastest_price = liquidity["asks"][0][0]
    # real_liquidity = liquidity["asks"][0][1]
    avg_liquidity = 0
    for i in liquidity["asks"]:
        avg_liquidity += float(i[1])
        real_liquidity = avg_liquidity
    return real_liquidity, lastest_price
            


# get_liquidity("BTCUSDT")

# import time

def manage_new_trade(orderbook, kill_switch):

    # Set variables
    order_long_id = ""
    order_short_id = ''
    signal_side = ''
    hot = False
    orders_long_placed = False  # Flag to track if orders are placed
    orders_short_placed = False

    # Get and save latest zscore
    # print("done")
    latest_zscore_infor = get_latest_zscore(orderbook)
    # print(latest_zscore_infor)
    enter_trade_zscore = latest_zscore_infor[0]
    # print("Current zscore:", enter_trade_zscore)
    signal_sign = latest_zscore_infor[1]

    enter_trade_spread = latest_zscore_infor[3]

    # Switch to hot if meets threshold
    if abs(enter_trade_zscore) > signal_trigger_thresh:
        # Activate hot trigger      
        hot = True
        print("Nong nong nong anh oy!")
        print("Vong 1:", enter_trade_zscore, "Vong 2:", enter_trade_spread)

    elif abs(enter_trade_zscore) < signal_trigger_thresh:
        print("Thoi anh, em nay bi giang mai, doi ti em tim cho con khac nha")
        hot = False
    
    # if not hot and kill_switch == 0:
    #     print("Current zscore is not hot:", enter_trade_zscore)

    if hot and kill_switch == 0:

        avg_liquidity_ticker_p, last_price_ticker_p = get_liquidity(signal_positive_ticker)
        avg_liquidity_ticker_n, last_price_ticker_n = get_liquidity(signal_negative_ticker)
        if float(last_price_ticker_n) > 10 or float(last_price_ticker_p) > 10:
            print("Last price is too high, please check the market, stop the program")

        price_precision_p, quantity_precision_p = get_precision(signal_positive_ticker)
        price_precision_n, quantity_precision_n = get_precision(signal_negative_ticker)

        if signal_sign:
            long_ticker = signal_positive_ticker
            short_ticker = signal_negative_ticker
            last_price_long = last_price_ticker_p
            avg_liquidity_long = avg_liquidity_ticker_p
            last_price_short = last_price_ticker_n
            avg_liquidity_short = avg_liquidity_ticker_n
        else:
            long_ticker = signal_negative_ticker
            short_ticker = signal_positive_ticker
            last_price_long = last_price_ticker_n
            avg_liquidity_long = avg_liquidity_ticker_n
            last_price_short = last_price_ticker_p
            avg_liquidity_short = avg_liquidity_ticker_p

        # Convert tradable capital quantity to tradable capital USDT
        tradeable_capital_ticker_long = usdt_to_crypto_quantity(tradeable_capital_usdt, long_ticker)
        tradeable_capital_ticker_short = usdt_to_crypto_quantity(tradeable_capital_usdt, short_ticker)

        # Fill targets
        capital_long = (tradeable_capital_ticker_long * 0.5)
        rounded_capital_long = round(capital_long, quantity_precision_n)
        capital_short = tradeable_capital_ticker_short * 0.5
        rounded_capital_short = round(capital_short, quantity_precision_p)
        notional_value_long = float(avg_liquidity_long) * float(last_price_long)
        notional_value_short = float(avg_liquidity_short) * float(last_price_short)
        initial_notional_injection_usdt = min(notional_value_long, notional_value_short)

        # Ensure initial capital does not exceed limit set in configuration
        if limit_order_basis:
            if initial_notional_injection_usdt > capital_long:
                initial_capital_usdt_long = rounded_capital_long
                initial_capital_usdt_short = rounded_capital_short
            else:
                initial_capital_usdt_long = initial_notional_injection_usdt
                initial_capital_usdt_short = initial_notional_injection_usdt
        else:
            initial_capital_usdt_long = rounded_capital_long
            initial_capital_usdt_short = rounded_capital_short

        remaining_capital_long = capital_long
        remaining_capital_short = capital_short
        print(initial_capital_usdt_short, initial_capital_usdt_long)
        # while kill_switch == 0:
        if not orders_long_placed and not orders_short_placed:  # Check if orders are already placed
            # Place order - long
            order_long_id = place_order(long_ticker, last_price_long, initial_capital_usdt_long, "Long")
            print(order_long_id)
            if order_long_id:
                remaining_capital_long -= initial_capital_usdt_long
                orders_long_placed = True

            # Place order - short
            order_short_id = place_order(short_ticker, last_price_short, initial_capital_usdt_short, "Short")
            print(order_short_id)
            if order_short_id:
                remaining_capital_short -= initial_capital_usdt_short
                orders_short_placed = True

            # Update signal side
            signal_side = "positive" if enter_trade_zscore > 0 else "negative"

            # Handle kill switch for market order
            if not limit_order_basis and orders_long_placed and orders_short_placed:
                kill_switch = 1

            # Allow for time to register the limit order
            time.sleep(1)

            # Check limit order and ensure zscore still within range
        zscore_new = get_latest_zscore(orderbook)
        # print(zscore_new, signal_sign_new)
        while kill_switch == 0:
            if abs(zscore_new[0]) > signal_trigger_thresh * 0.9 and zscore_new[1] == signal_sign:

                # Check long order status
                if orders_long_placed:
                    order_status_long = check_order(long_ticker, order_long_id, remaining_capital_long, "Long")
                    # print(order_status_long)
                # Check short order status
                if orders_short_placed:
                    order_status_short = check_order(short_ticker, order_short_id, remaining_capital_short, "Short")
                print(order_status_short, order_status_long, zscore_new)
                # If order still active then do nothing
                if order_status_long == "Order active" or order_status_short == "Order active":
                    continue
                # If order partial fill then do nothing
                if order_status_long == "Position Filled" or order_status_short == "Position Filled":
                    continue
                # If order filled then do nothing
                if order_status_long == "Trade completed" and  order_status_short == "Trade completed":
                    kill_switch = 1

                # If position filled - place new order
                if order_status_long == "Position Filled" and order_status_short == "Position Filled":
                    orders_placed = False

                # If order canceled for long - try again
                if order_status_short == "Try again":
                    orders_placed = False

                # If order canceled for short - try again
                if order_status_long == "Try again":
                    orders_placed = False
            else:
                
                # Cancel all active order
                client.futures_cancel_all_open_orders(symbol=signal_positive_ticker)
                client.futures_cancel_all_open_orders(symbol=signal_negative_ticker)
                kill_switch = 1

        
    # Output status
    return kill_switch, signal_side, enter_trade_zscore, enter_trade_spread
