from func_calculation import get_trade_details
from func_prices_call import get_price_klines
from func_stats import calculate_spread_coint
from config_execution_api import ticker_1, ticker_2, signal_positive_ticker, signal_negative_ticker
import numpy as np
import time
import math
import pandas as pd

def get_latest_zscore(orderbook):

    # print(orderbook["s"])
    
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
        
        
        coint_flag, spread, zscore_list = calculate_spread_coint(series_1, series_2) # zscore_list = 
        # spread_df = pd.DataFrame(spread)
        # # print(spread_df)
        zscore = zscore_list[-1]
        spread_new = spread[-1]
        # print(spread_new)
        # spread_new = spread_df.iat[-1,1]
        # print(zscore)
    #         # print(zscore)
        if zscore > 0 and spread_new > 0:
                signal_sign = True # positive
        elif zscore < 0 and spread_new < 0:
            signal_sign = False # negative
    #     # print(zscore, signal_sign)
        time.sleep(1)
    return zscore, signal_sign, zscore_list, spread_new

    # series_1, series_2 = get_price_klines()
    # # Get latest asset orderbook prices and add dummy price for latest
    # pass