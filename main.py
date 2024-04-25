import warnings
from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
from func_cointegration import get_cointegrated_pairs
import json
import pandas as pd
warnings.simplefilter(action="ignore",category= FutureWarning)

"""Chien luoc giao dich"""
if __name__ == "__main__":

    # # Step 1 - Get list of symbols
    # print("Getting symbols...")
    # sym_response = get_tradeable_symbols()
    
    # # Step 2 - Construct and save price history
    # print("Constructing and saving price data to JSON..")
    # if len(sym_response) > 0:
    #     store_price_history(sym_response)

    # Step 3 - Find Cointegrated Pairs
    print("Finding Cointegrated Pairs...")

    def get_variable_type(var):
        return type(var)
    dictionaries = []

    # Open the JSON file
    with open("price_history.json") as json_file:

    #     # Load the data from the JSON file
        price_data = json_file.read()
        
    #     dictionaries.append(price_data)
        if len(price_data) > 0:
            coint_pairs = get_cointegrated_pairs(price_data)
        
        