import requests
from classes.ErrorMessages import *
from datetime import date
import numpy as np
import time

class CryptoCurrency:

    cryptoIDs = ["bitcoin", "ethereum", "polkadot", "cardano", "metal", "binancecoin", "ripple", "dogecoin"]    

    def __init__(self, id):
        if id not in CryptoCurrency.cryptoIDs:
            raise  ValueError(ErrorMessages.get_crypto_id_error())
        self.id = id

    #Request with less than 0 days still work so we are handling it ourselves
    #Same thing with interval, only daily as a parameter is accetable
    def get_prices(self, vs_currency, days, interval=None):

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

        avg = self.get_MA(data)
        times = [time.strftime('%Y-%m-%d %H:%M', time.gmtime(float(tup[0]) / 1e3)) for tup in data['prices']]
        data['prices'] = list(map(lambda x: x[1], data['prices']))
        result = {
            "prices": data['prices'],
            "time": times,
            "interval": interval,
            "vs_currency": vs_currency,
            "days": days,
            "SMA_3": avg['SMA_3'],
            "SMA_4": avg['SMA_4'],
        }
        
        return result

    def get_single_value(self):
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + self.id + '&vs_currencies=usd'
        data = requests.get(url).json()

        if "error" in data:
            return ErrorMessages.handle_CoinGecko_error(data)

        return float(data[self.id]['usd'])
        

    def get_interval(self, days):
        days = int(days)
        if days <= 1:
            return "minutely"
        elif days > 1 and days <= 90:
            return "hourly"
        else:
            return "daily"

    def get_info(self):
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

        result = {
            "icon": data['image']['small']
        }

        return result
    
    def get_MA(self, data):
        n = len(data['prices'])
        SMA_3 = [None for _ in range(n)]
        SMA_4 = [None for _ in range(n)]

        for i in range(n-2):
            SMA_3[i + 2] = np.round(((data['prices'][i][1] + data['prices'][i+1][1] + data['prices'][i+2][1])/3),1)
        for i in range(n-3):
            SMA_4[i + 3] = np.round(((data['prices'][i][1] + data['prices'][i+1][1] + data['prices'][i+2][1] + data['prices'][i+3][1])/4),1)

        return {'SMA_3' : SMA_3,
                'SMA_4' : SMA_4}


    