from config_strategy_api import *

# Get symbols that are tradeable
def get_tradeable_symbols():
    sym_list = []

    # Get symbols with trading status from get spot exchange info
    spot_exchange_info = get_spot_exchange_info()
    # print(spot_exchange_info)
    # if spot_exchange_info:
    symbols = spot_exchange_info.get('symbols', [])
    for symbol in symbols:
    #         # print(symbol)
            if symbol.get('status') == 'TRADING' and symbol.get('quoteAsset') == 'USDT':
                # append only first 5 symbols
                # if len(sym_list) < 5:
                #     sym_list.append(symbol['symbol'])
                # else:
                #     break

                sym_list.append(symbol['symbol'])
    
    # from sym_list, get symbols with trading status from get futures exchange info with get_ticker_info
    new_list = []
    for sym in sym_list:
        if get_ticker_info(sym):
            # new_list.append(get_ticker_info(sym))
            # select only symbol with contractType == "PERPETUAL"
            if get_ticker_info(sym).get('contractType') == "PERPETUAL" and get_ticker_info(sym).get('status') == "TRADING":
                symbol = get_ticker_info(sym).get('symbol')
                new_list.append(symbol)

    # print(new_list)
    return new_list #return new_list # Corrected new list

