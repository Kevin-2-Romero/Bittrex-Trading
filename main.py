from Database import Database
import Platform
import numpy as np
from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as datetime

testBit = Platform.Bittrex('redacted', 'redacted')
bDB = Database(testBit, '/home/kevin/Development/TradingBot/Crypto_Markets/Bittrex_Market.db')
stockData = np.array([x[1::] for x in bDB.selectValues('BTC-LTC', 'day')])

fig, ax = plt.subplots()
candlestick2_ohlc(ax, stockData, width=0.6)
fig.tight_layout()
plt.show()
