from func_position_calls import get_avtive_positions, get_open_orders
from config_execution_api import client

# Checko order items
def check_order(ticker, order_id, remaining_capital, direction = "Long"):

    # Get trade details
    open_orders_information = client.futures_get_order(symbol = ticker, orderId=order_id)


    # Get open position
    active_position_information = get_avtive_positions(ticker = ticker)
    
    # Determine action - trade completer -> stop placing order
    if active_position_information[0] >= remaining_capital or open_orders_information['status'] == "FILLED":
        return "Trade completed"
    
    # Determine action - position filled -> buy more
    if open_orders_information['status'] == "FILLED":
        return "Position Filled"
    
    # Determine action -  do nothing
    if open_orders_information['status'] == "PARTIALLY_FILLED" or "NEW" or "EXPIRED_IN_MATCH":
        # Change order type to market
        return "Order active"
    
    # Determine action - try to place order
    if open_orders_information['status'] == "CANCELED" or "EXPIRED" or "REJECTED":
        return "Try again" 


    # Deter

    
    
    

    
