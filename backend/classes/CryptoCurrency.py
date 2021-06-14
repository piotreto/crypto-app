import requests
from classes.ErrorMessages import *
import datetime
import numpy as np
import time
# from time import datetime

class CryptoCurrency:

    cryptoIDs = ["bitcoin", "ethereum", "polkadot", "cardano", "metal", "binancecoin", "ripple", "dogecoin"]    

    def __init__(self, id):
        if id not in CryptoCurrency.cryptoIDs:
            raise  ValueError(ErrorMessages.get_crypto_id_error())
        self.id = id

    #Request with less than 0 days still work so we are handling it ourselves
    #Same thing with interval, only daily as a parameter is accetable
    def get_prices(self, vs_currency, days, interval=None):
        """returns prices ina given intervals and currency of crypto"""

        if int(days) < 0:
            return ErrorMessages.get_days_error()
            
        
        if interval == None:
            url = "https://api.coingecko.com/api/v3/coins/" + self.id + "/market_chart?vs_currency=" + vs_currency + "&days=" + days
            interval = self.get_interval(days)
        elif (interval != 'daily'):
            return ErrorMessages.get_interval_error()
        else:
            url = "https://api.coingecko.com/api/v3/coins/" + self.id + "/market_chart?vs_currency=" + vs_currency + "&days=" + days + "&interval=" + interval

            
        data = requests.get(url).json()

        if "error" in data:
            return ErrorMessages.handle_CoinGecko_error(data)

        #CoinGecko API give us 1 price element more everytime, so we are getting rid of it
        data['prices'].pop(0)

        # for tup in data['prices']:
        #     print(time.strftime('%Y-%m-%d', time.gmtime(float(tup[0]) / 1e3)))

        # avg = self.get_MA(data)
        times = [time.strftime('%Y-%m-%d %H:%M', time.gmtime(float(tup[0]) / 1e3)) for tup in data['prices']]
        data['prices'] = list(map(lambda x: x[1], data['prices']))
        result = {
            "prices": data['prices'],
            "time": times,
            "interval": interval,
            "vs_currency": vs_currency,
            "days": days,
            "SMA_7": self.get_MA(data, 7),
            "SMA_25": self.get_MA(data, 25),
            "SMA_99": self.get_MA(data, 99),
            "logo": self.get_logo_url()
        }
        
        return result

    def get_single_value(self):
        """returns actual price of a crypto"""
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + self.id + '&vs_currencies=usd'
        data = requests.get(url).json()
        print(data)

        if "error" in data:
            return ErrorMessages.handle_CoinGecko_error(data)

        return float(data[self.id]['usd'])
        
    def get_interval(self, days):
        '''
        Gets the interval type for the number of days according to CoinGecko documentation
        
        days: number of days
        ''' 
        days = int(days)
        if days <= 1:
            return "minutely"
        elif days > 1 and days <= 90:
            return "hourly"
        else:
            return "daily"

    def get_info(self):
        '''
        Gets the information about our crypto
        '''
        url = "https://api.coingecko.com/api/v3/coins/" + self.id
        data = requests.get(url).json()

        if "error" in data:
            return ErrorMessages.handle_CoinGecko_error(data)
        
        
        result = {
            "id": data['id'],
            "symbol": data['symbol'],
            "name": data['name'],
            "description": data['description']['en']
        }
        
        return result
    
    def get_logo_url(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday = yesterday.strftime('%d-%m-%Y')

        url = "https://api.coingecko.com/api/v3/coins/" + self.id + "/history?date=" + str(yesterday)
        data = requests.get(url).json()

        if "error" in data:
            return ErrorMessages.handle_CoinGecko_error(data)

        # result = {
        #     "icon": data['image']['small']
        # }

        return data['image']['small']
    
    def get_MA(self, data, window_size):
        """get moving average of a crypto"""
        n = len(data['prices'])
        SMA = [None for _ in range(window_size-1)]

        i = 0
        moving_averages = 0
        while i < n - window_size + 1:
            this_window = data['prices'][i: i + window_size]

            window_average = sum(this_window) / window_size
            SMA.append(window_average)
            i += 1
        return SMA


    def get_previous_day_price(self):
        """get prive of a crypto in previous day"""
        data = self.get_prices("usd", "10")

        return data['prices'][-25]

    @staticmethod
    def get_all_current_prices():
        '''Gets prices for all cryptos that we are considering (method created)'''
        resultString = '%2C'.join(CryptoCurrency.cryptoIDs) 
        
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + resultString + '&vs_currencies=usd'
        data = requests.get(url).json()
        print(data)
        return data


    