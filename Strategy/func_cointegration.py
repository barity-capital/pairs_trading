import json
from config_strategy_api import z_score_window
from config_strategy_api import get_spot_exchange_info, query_mark_price_kline
from func_get_symbols import get_tradeable_symbols
import math
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

def calculate_cointegration(series1, series2):
    coint_flag = 0
    coint_res = coint(series1, series2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series1, series2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series1, series2, hedge_ratio)
    
    zero_crossing = len(np.where(np.diff(np.sign(spread)))[0])
    # print(zero_crossing)
    if p_value < 0.05 and coint_t < critical_value:
        coint_flag = 1
    # print( (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), round(hedge_ratio, 2),zero_crossing))
    return (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), round(hedge_ratio, 2),zero_crossing)
    

# Put close prices into a list
def extract_close_prices(prices):
    # pass
    close_prices = []
    
    # print(price_data)
    for i in prices:
        if math.isnan(i):
            return []
        # append only same length i to close price

        close_prices.append(i)
    # print(close_prices)
    return close_prices    

def normalize(values):
    # Find the minimum and maximum values in the list
    min_val = min(values)
    max_val = max(values)
    
    # Normalize each value to the range [0, 1]
    normalized_values = [(val - min_val) / (max_val - min_val) for val in values]
    
    return normalized_values

# Calculate Cointegrated Pairs
def get_cointegrated_pairs(prices):
    # pass
    # Loop through coins and check for co-integration
    coint_pair_list =[]
    included_list = []
    for sym1 in prices.keys():
        
        # Check each coin against the first (sym1)
        for sym2 in prices.keys():
            if sym1 != sym2:
                
                # Get unique combination ID and ensure one off check
                sorted_characters = sorted(sym1 + sym2)
                unique = "".join(sorted_characters)
                if unique in included_list:
                    break
                
                # Get close prices
                series_1 = extract_close_prices(prices[sym1])
                series_2 = extract_close_prices(prices[sym2])
                if len(series_1) == len(series_2) and len(series_1) > 0:
                # Check for cointegration and add cointegrated pair
                    # coint_result = calculate_cointegration(normalize(series_1), normalize(series_2))
                    coint_result = calculate_cointegration(series_1, series_2)
                    if coint_result[0] == 1:
                        included_list.append(unique)
                        coint_pair_list.append({
                            "sym_1": sym1,
                            "sym_2": sym2,
                            "p_value": coint_result[1],
                            "t_value": coint_result[2],
                            "critical_value": coint_result[3],
                            "hedge_ratio": coint_result[4],
                            "zero_crossing": coint_result[5],
                            # "spread": coint_result[5],
                            # "residuals": coint_result[7]
                        })
                    
    # Output results
    df_coint = pd.DataFrame(coint_pair_list)        
    df_coint = df_coint.sort_values("zero_crossing", ascending=False)
    df_coint.to_csv("2_cointegrated_pairs.csv")
    return df_coint