# from func_prices_klines import get_prices_klines
from func_get_symbols import get_tradeable_symbols
from config_strategy_api import  query_mark_price_kline
import json

# Store price history for all available symbols
def store_price_history(symbols):
    price_history_dict = {}

    for sym in symbols:
        kline_info = query_mark_price_kline(sym, '1h')
        close_prices = [float(entry[4]) for entry in kline_info]  # Extracting close prices
        price_history_dict[sym] = close_prices
    if len(price_history_dict) > 0:
        with open('price_history.json', "w") as fp:
            json.dump(price_history_dict, fp, indent=4)
        print("Prices saved successfully")
    return


    # for sym in symbols:
    #     kline_info = query_mark_price_kline(sym, '1h')
    #     # Get index 4 in every array in array close_price
    #     for item in kline_info:
    #         # for i in item:
    #     # close_price.append(kline_info[0][4])
    #         return item

        # Join sym key with close_price value
        # price_history_dict[sym] = close_price

    # print(close_price)
# store_price_history("BTCUSDT")

        # print(sym)
        # symbol = sym['symbol']
        # interval = '1h'  # Example interval, you can modify this as needed
        # klines = query_mark_price_kline(symbol, interval)
        # print(klines)
        
    #     if klines:
    #         price_history_dict[symbol] = klines
    #         # append to json file with symbol as key
    #         with open('price_history.json', 'w') as f:
    #             f.write(json.dumps({symbol: klines}, indent=4) + '\n')
    #             # add "," after each object in json file
    #             # if price_history_dict[symbol] != symbols[-1]:
    #             #     f.write(',')
    #         print("Prices saved successfully")
    #     else:
    #         print(f"Failed to fetch klines for symbol: {symbol}")
    # return
    
    # Now price_history_dict contains klines for each symbol
    





