import json
from config_strategy_api import get_spot_exchange_info
import math


# Put close prices into a list
def extract_close_prices(prices):
     pass
    #  close_prices = []
    #  for price_values in prices:
    #     if math.isnan(price_values[])

# Calculate Cointegrated Pairs
def get_cointegrated_pairs(prices):
    sym_list = []
    included_list = []
    # Get symbols with trading status from get spot exchange info
    spot_exchange_info = get_spot_exchange_info()
    # print(spot_exchange_info)
    # if spot_exchange_info:
    symbols = spot_exchange_info.get('symbols', [])
    for symbol in symbols:
            
    #         # print(symbol)
            if symbol.get('status') == 'TRADING' and symbol.get('quoteAsset') == 'USDT':
                sym_list.append(symbol['symbol'])
                for sym1 in sym_list:
                    for sym2 in sym_list:
                        if sym1 != sym2:
                            
                            # Get unique combination id and ensure one off check
                            sorted_characters = sorted(sym1 + sym2)
                            unique = "".join(sorted_characters)
                            if unique in included_list:
                                 break
                            
                            print(prices[sym1])
                            # # Get close prices
                            # series_1 = extract_close_prices(prices[sym1])
                            # series_2 = extract_close_prices(prices[sym2])