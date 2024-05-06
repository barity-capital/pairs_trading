import warnings
from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
from func_cointegration import get_cointegrated_pairs, extract_close_prices, calculate_spread
from func_plot_trends import plot_trends
import json
import pandas as pd
warnings.simplefilter(action="ignore",category= FutureWarning)

"""Chien luoc giao dich"""
if __name__ == "__main__":

    # Step 1 - Get list of symbols
    # print("Getting symbols...")
    # sym_response = get_tradeable_symbols()
    
    # # Step 2 - Construct and save price history
    # print("Constructing and saving price data to JSON..")
    # if len(sym_response) > 0:
    #     store_price_history(sym_response)

    #Step 3 - Find Cointegrated Pairs
    # print("Finding Cointegrated Pairs...")

    # # Open the JSON file
    # with open("price_history.json", "r") as file:
    #     price_data = json.load(file) 
    #     if len(price_data) > 0:
    #         coint_pairs = get_cointegrated_pairs(price_data)
        
    # Step 4: plot trends and save for backtesting
    print("Plotting trends...")
    symbol_1 = "OCEANUSDT"
    symbol_2 = "AGIXUSDT"
    with open("price_history.json") as file:
        price_data = json.load(file)
        if len(price_data) > 0:
            plot_trends(symbol_1, symbol_2, price_data)