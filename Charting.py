from Database import Database
import numpy as np
from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as datetime
from Database import Database

# data from dataTable returned as:
# ticker('BTC-LTC') 
# datastamp('%Y-%M-%DT%H:%M:%S')
# open(everything is float)
# high
# low
# close
# vol
# bvol
# 
# selectValues returns:
# [(ticker, datetime, open, high, low, close, vol, bvol), (...), (...)]
#
# tickerData = np.array(**(dataBase.selectValues(ticker, tickerInt)))

