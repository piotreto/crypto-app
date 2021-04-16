import requests
import . from ErrorMessages
from datetime import date

class CryptoCurrency:

    cryptoIDs = ["bitcoin", "ethereum", "polkadot", "cardano", "metal", "binancecoin", "ripple", "dogecoin"]    

    def __init__(self, id):
        if id not in CryptoCurrency.cryptoIDs:
            raise  ValueError(ErrorMessages.get_crypto_id_error())
        self.id = id

    #Request with less than 0 days still work so we are handling it ourselves
    #Same thing with interval, only daily as a parameter is accetable
    def get_prices(self, vs_currency, days, interval=None):

        if days < 0:
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
       
        result = {
            "prices": data['prices'],
            "interval": interval,
            "vs_currency": vs_currencyError,
            "days": days
        }
        
        return result

    def get_interval(self, days):
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
        
    def get_macd(self):

    