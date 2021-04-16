class ErrorMessages:

    errorMessages = {
        "methodError": {
            "error": "This method is unavaliable"
        },
        "cryptoIdError": {
            "error": "Cryptocurrency with this id doesn't exists"
        },
        "vs_currencyError": {
            "error": "vs_currency with this id doesn't exists"
        },
        "daysError": {
            "error": "Wrong days amount"
        },
        "intervalError": {
            "error": "Wrong type of interval"
        }
    }

    @staticmethod
    def handle_CoinGecko_error(data):
        if data['error'] ==  "Could not find coin with the given id":
            return ErrorMessages.get_crypto_id_error()
        elif data['error'] == "invalid vs_currency":
            return ErrorMessages.get_vs_currency_error()
        else:
            returun data['error']

            

    @staticmethod
    def get_method_error():
        return errorMessages['methodError']
    
    @staticmethod
    def get_crypto_id_error():
        return errorMessages['cryptoIdError']

    @staticmethod
    def get_vs_currency_error():
        return errorMessages['vs_currencyError']

    @staticmethod
    def get_days_error():
        return ErrorMessages['daysError']
    
    @staticmethod
    def get_interval_error():
        return ErrorMessages['intervalError']