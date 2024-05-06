import json
from config_execution_api import z_score_window
# from config_strategy_api import get_spot_exchange_info, query_mark_price_kline
# from func_get_symbols import get_tradeableco_symbols
# import math
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd
import numpy as np



def calculate_spread(series1, series2, hedge_ratio):
    spread = pd.Series(series1) - (pd.Series(series2) * hedge_ratio)
    return spread

def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()
    x = df.rolling(center=False, window = 1).mean()
    df["ZSCORE"] = (x-mean) / std
    return df["ZSCORE"].astype(float).values

def calculate_zscore_coint(series1, series2):
    coint_flag = 0
    coint_res = coint(series1, series2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series1, series2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series1, series2, hedge_ratio)
    
    zscore_list = calculate_zscore(spread)
    # print(zero_crossing)
    if p_value < 0.05 and coint_t < critical_value:
        coint_flag = 1
    # print( (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), round(hedge_ratio, 2),zero_crossing))
    return coint_flag, zscore_list.tolist()

