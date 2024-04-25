# from func_prices_klines import get_prices_klines
from func_get_symbols import get_tradeable_symbols
from func_prices_klines import query_mark_price_kline
import json

# Store price history for all available symbols
def store_price_history(symbols):
    
    price_history_dict = {}
    for sym in symbols:
        symbol = sym['symbol']
        interval = '1h'  # Example interval, you can modify this as needed
        klines = query_mark_price_kline(symbol, interval)
        
        if klines:
            price_history_dict[symbol] = klines
            # append to json file with symbol as key
            with open('price_history.json', 'a') as f:
                f.write(json.dumps({symbol: klines}, indent=4) + '\n')
                # add "," after each object in json file
                if price_history_dict[symbol] != symbols[-1]:
                    f.write(',')
            print("Prices saved successfully")
        else:
            print(f"Failed to fetch klines for symbol: {symbol}")
    return
    
    # Now price_history_dict contains klines for each symbol
    





