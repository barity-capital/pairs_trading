from func_calculation import get_trade_details
from func_prices_call import get_price_klines
from func_stats import calculate_zscore_coint
from config_execution_api import ticker_1, ticker_2, signal_positive_ticker, signal_negative_ticker
import numpy as np

def get_latest_zscore(orderbook):
    mid_price_long = get_trade_details(orderbook, direction="Long")    
    mid_price_short = get_trade_details(orderbook, direction="Short")    

    # print(mid_price_long, mid_price_short)
    # print(orderbook["s"])
    series_1, series_2 = get_price_klines()
    # print(series_1)

    # Get zscore and confirm it's hot
    # if len(series_1) > 0 and len(series_2) > 0:
    if series_1 is not None and series_2 is not None:
        # Ensure series have the same length
        min_length = min(len(series_1), len(series_2))

        
        series_1 = series_1[:min_length]
        series_1.pop()
        # print(series_1)
        series_1.append(mid_price_long[0])
        # print(series_1)
        # Trim the last element in series_1
        
        series_2 = series_2[:min_length]
        series_2.pop()
        series_2.append(mid_price_short[0])
        
        
    # if orderbook["s"].lower() == signal_positive_ticker:
    #     mid_pice = get_trade_details(orderbook)
    #     # print(mid_price[0])
    #     # Append mid price to series

    #     series_1.append(mid_pice[0])
    #     print(series_1)
    #     # convert to numpy array
    #     # trimmed_series_1 = 
    #     # np.array(trimmed_series)
    # if orderbook["s"].lower() == signal_negative_ticker:
    #     mid_pice = get_trade_details(orderbook)
    #     series_2.append(mid_pice[0])
        # for string_price in series_2:
        #     string_price = float(string_price)
        # series_2.append(mid_pice[0])
            # trimmed_series_2 = np.array(trimmed_series)
    # print(series_1, series_2)
    zscore_list = calculate_zscore_coint(series_1, series_2)
    # print(zscore_list)
    zscore = zscore_list[1][-1]
        # print(zscore)
    if zscore > 0:
            signal_sign = True
    else:
        signal_sign = False
    # print(zscore, signal_sign)
    return zscore, signal_sign, zscore_list

    # series_1, series_2 = get_price_klines()
    # # Get latest asset orderbook prices and add dummy price for latest
    # pass