import sqlite3

class Database:

  def __init__(self, platform, dbFile):
    self.db = dbFile
    self.platform = platform
    self.tickIntervals = (self.platform).tickIntervals

  def update(self, ticker, tickerInterval):
    self.conn = sqlite3.connect(self.db)
    self.c = (self.conn).cursor()
    self.tableName = tickerInterval
    self.ticker = ticker

    try:
      self.s_comm = "SELECT datestamp FROM {0} WHERE ticker = '{1}'".format(self.tableName, self.ticker)
      (self.c).execute(self.s_comm)
      self.r = (self.c).fetchall()
      self.lastDate = ((self.r)[len(self.r) - 1])[0]
      print('Last date is: ' + self.lastDate)

    except:
      print('*** Unable to locate most recent tick, will complete full update ***')
      self.lastDate = '0000-00-00T00:00:00'
      print('Creating table...')
      self.create_comm = "CREATE TABLE IF NOT EXISTS {0} (ticker TEXT, datestamp TEXT, open REAL, high REAL, low REAL, close REAL, volume REAL, bvolume REAL)".format(self.tableName)
      (self.c).execute(self.create_comm)
    self.address = ((self.platform).requestPoint['GetTicks']).format(ticker, tickerInterval)
    self.tickList = (self.platform).sendRequest(False, self.address)
    self.counter = 0
    for candle in (self.tickList)['result']:
      self.t = candle['T']
      if (self.t > self.lastDate):
        self.entry = "INSERT INTO {0} VALUES (?, ?, ?, ?, ?, ?, ?, ?)".format(self.tableName)
        (self.c).execute((self.entry), (ticker, candle['T'], candle['O'], candle['H'], candle['L'], candle['C'], candle['V'], candle['BV']))
        self.counter+=1
    (self.conn).commit()
    print('New ticks added: ', self.counter)
    print('--------------- Finished Updates ---------------')
    (self.c).close()
    (self.conn).close()

  def selectValues(self, ticker, tickerInterval):
    self.conn = sqlite3.connect(self.db)
    self.c = (self.conn).cursor()
    self.selectCom = "SELECT * FROM {0} WHERE ticker = '{1}'".format(tickerInterval, ticker)
    (self.c).execute(self.selectCom)
    self.r = (self.c).fetchall()
    return self.r
    (self.c).close()
    (self.conn).close()
