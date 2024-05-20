# Remove Pandas future warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# General imports
import pandas as pd
import numpy as np
from config_execution_api import * 
from func_position_calls import *

# from pandas_datareader import data as pdr
# import datetime
# import os
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# General
from config_execution_api import signal_negative_ticker
from config_execution_api import signal_positive_ticker
from func_position_calls import open_order_confirmation
from func_position_calls import active_position_confirmation
from func_trade_management import manage_new_trade
from func_execution_calls import set_leverage
from func_close_position import close_all_positions
from func_save_status import save_status
import time


""" RUN START """


