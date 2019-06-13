import random
import time
from calendar import timegm
import requests
import hmac
import hashlib




class Bittrex:

  def __init__(self, secretAPIKey, publicAPIKey):
    self.tickIntervals = ["oneMin", "fiveMin", "thirtyMin", "hour", "day"]
    self.API_secret = secretAPIKey
    self.API_public = publicAPIKey
    self.openOrders = {}
    self.requestPoint = {
        # Public API--------------------------------------------------------------------------------
        'pingBittrex': 'https://socket.bittrex.com/signalr/ping',
        'APIVersion': 'https://bittrex.com/Content/version.txt',
        'GetCurrencies': 'https://bittrex.com/api/v2.0/pub/currencies/GetCurrencies',
        'GetMarkets': 'https://api.bittrex.com/api/v1.1/public/getmarkets',
        'GetMarketSummaries': 'https://bittrex.com/api/v2.0/pub/markets/GetMarketSummaries',
        'GetMarketSummary': 'https://bittrex.com/Api/v2.0/pub/market/GetMarketSummary?marketName={0}',
        'GetTicks': 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={0}&tickInterval={1}',
        'GetLatestTick': 'https://bittrex.com/Api/v2.0/pub/market/GetLatestTick?marketName={0}&tickInterval={1}',
        'GetMarketHistory': 'https://bittrex.com/api/v2.0/pub/market/GetMarketHistory?marketName={0}',
        'GetOrderBook': 'https://bittrex.com/api/v1.1/public/getorderbook?market={0}C&type={1}',
        # Market API--------------------------------------------------------------------------------
        'BuyLimit': 'https://bittrex.com/api/v1.1/market/buylimit?apikey={0}&market={1}&quantity={2}&rate={3}',
        'SellLimit': 'https://bittrex.com/api/v1.1/market/selllimit?apikey=API_KEY&market=BTC-LTC&quantity=1.2&rate=1.3',
        'CancelOrder': 'https://bittrex.com/api/v1.1/market/cancel?apikey={0}&uuid={1}',
        'GetOpenOrders': 'https://bittrex.com/api/v1.1/market/getopenorders?apikey={0}&market={1}',
        # Account API--------------------------------------------------------------------------------
        'GetBalances': 'https://bittrex.com/api/v1.1/account/getbalances?apikey={0}',
        'GetBalance': 'https://bittrex.com/api/v1.1/account/getbalance?apikey={0}&currency={1}',
        'GetDepositAddress': 'https://bittrex.com/api/v1.1/account/getdepositaddress?apikey={0}&currency={1}',
        'Withdraw': 'https://bittrex.com/api/v1.1/account/withdraw?apikey={0}&currency={1}&quantity={2}&address={3}',
        'GetOrder': 'https://bittrex.com/api/v1.1/account/getorder&uuid={0}',
        'GetOrderHistory': 'https://bittrex.com/api/v1.1/account/getorderhistory?apikey={0}',
        'GetWithdrawalHistory': 'https://bittrex.com/api/v1.1/account/getwithdrawalhistory?apikey={0}currency={1}',
        'GetDepositHistory': 'https://bittrex.com/api/v1.1/account/getdeposithistory?currency={0}'
    }

  # Authentication------------------------------------------------------------

  def epoch(self):
    return str(int(timegm(time.gmtime())))

  def apiSign(self, privateKey, url):
    return hmac.new(privateKey.encode(), url.encode(), hashlib.sha512).hexdigest()

  def sendRequest(self, auth, address):
    self.nonce = self.epoch()
    self.address = address
    if ('v2.0' in address):
      self.address = address + '&nonce={0}'.format(self.nonce)
      # print('v2.0')
      print(self.address)
    elif ('v1.1' in self.address):
      self.address = address + '&nonce={0}'.format(self.nonce)
      # print('v1.1')
      # print(self.address)
    if auth == True:
      # print('auth true')
      self.signature = self.apiSign(self.API_secret, self.address)
      self.h = {'apisign': self.signature}
      return (requests.get(self.address, headers=self.h).json())
    elif auth == False:
      # print('auth false')
      return ((requests.get(self.address)).json())

  # Public Requests------------------------------------------------------------

  def getCurrencies(self):
    (self.sendRequest(False, 'https://bittrex.com/api/v1.1/public/getcurrencies'))

  def getMarkets(self):
      return (requests.get('https://api.bittrex.com/api/v1.1/public/getmarkets')).json()
  def getMarketSummaries(self, **kwargs):
    pass

  def getTicks(self, marketName, tickInterval):
    return self.sendRequest(False, self.requestPoint['GetTicks'].format(marketName, tickInterval))

  def getLatestTick(self, marketName, tickInterval):
    self.tickAddress = (self.requestPoint['GetLatestTick']).format(marketName, tickInterval)
    return self.sendRequest(self.tickAddress)

  def getMarketHistory(self, marketName):
    self.marketHistoryURL = (self.requestPoint['GetMarketHistory']).format(marketName)
    return self.sendRequest(self.marketHistoryURL)

  def getOrderBook(self, market, typeOfTrade):
    self.orderBookURL = (self.requestPoint['GetOrderBook']).format(market, typeOfTrade)
    return self.sendRequest(self.orderBookURL)

  # Market Requests------------------------------------------------------------

  def trade(self, pos, market, amount, rate):
    if (pos == 'buy'):
      self.tradeURL = ((self.requestPoint)['BuyLimit']).format(self.API_public, market, amount, rate)
    elif (pos == 'sell'):
      self.tradeURL = ((self.requestPoint)['SellLimit']).format(self.API_public, market, amount, rate)
    try:
      self.trade = (self.sendRequest(True, self.tradeURL)).json
      self.openOrders[(self.trade)['result']] = {'type': pos, 'market': market, 'amount': amount, 'rate': rate}
      print('-- Trade was placed successfully --')
    except:
      print('[ERROR] Unable to place trade')

  def cancelOrder(self, uuid):
    self.cancelURL = (self.requestPoint['CancelOrder']).format(uuid)
    self.sendRequest(True, self.cancelURL)

  def getOpenOrders(self, market):
    self.getOpenOrdersURL = (self.requestPoint['GetOpenOrders']).format(self.API_public, market)
    self.sendRequest(True, self.getOpenOrdersURL)

  # Account Requests------------------------------------------------------------

  def orderHistory(self, market):
    if (market == 'all'):
      print((self.sendRequest((self.requestPoint)['GetOrderHistory'].format(self.API_public))))
    else:
      self.orderHistoryURL = (self.requestPoint['GetOrderHistory'] + '&market={0}'.format(market))
      print((self.sendRequest(self.orderHistoryURL)))

  def viewBalance(self, *args):
    if (len(args) == 1):
      self.getBalance = (self.requestPoint['GetBalance']).format(self.API_public, args)
    elif (len(args) > 1):
      self.balanceURL = (self.requestPoint['GetBalances']).format(self.API_public)
      for currency in (self.sendRequest(self.balanceURL))['result']:
        if currency['Currency'] in args:
          print(currency)
    elif (len(args) == 0):
      self.balanceURL = (self.requestPoint['GetBalances']).format(self.API_public)
      print((self.sendRequest(True, self.balanceURL)))

  def getDepositAddress(self, currency):
    self.depositAddressURL = (self.requestPoint['GetDepositAddress']).format(self.API_public, currency)
    self.sendRequest(self.depositAddressURL)

  def withdraw(self):
    pass

  def getOrder(self, uuid):
    self.orderURL = (self.requestPoint['GetOrder']).format(uuid)
    self.sendRequest(self.orderURL)

  def getWithdrawalHistory(self, currency):
    self.wHistoryURL = (self.requestPoint['GetWithdrawalHistory']).format(self.API_public, currency)
    self.sendRequest(self.wHistoryURL)

  def getDepositHistory(self, currency):
    self.dHistoryURL = (self.requestPoint['GetDepositHistory']).format(currency)
    self.sendRequest(self.dHistoryURL)

