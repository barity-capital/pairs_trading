from config_execution_api import *
from binance.client import Client
# Create a function to return position info by passing api_url

def get_position_info():
    client = Client(api_key, api_secret)

    position_info = client.futures_position_information()
    for i in position_info:
        if float(i["positionAmt"]) != 0.0000:
            current_position = float(i["positionAmt"])
    return current_position
get_position_info()