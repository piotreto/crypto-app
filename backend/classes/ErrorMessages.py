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
        },
        "duplicateEmailError": {
            "error": "Email already exists"
        },
        "emailError": {
            "error": "Invalid email"
        },
        "passwordError": {
            "error": "Invalid password"
        },
        "jwtError": {
            "error": "JWT is not valid"
        }, 
        "moneyError": {
            "error": "Not enough currency!"
        },
        "negativeError":{
            "error": "Negative value is forbidden!"
        } 
    }

    @staticmethod
    def handle_CoinGecko_error(data):
        if data['error'] ==  "Could not find coin with the given id":
            return ErrorMessages.get_crypto_id_error()
        elif data['error'] == "invalid vs_currency":
            return ErrorMessages.get_vs_currency_error()
        else:
            return data['error']

            

    @staticmethod
    def get_method_error():
        return ErrorMessages.errorMessages['methodError']
    
    @staticmethod
    def get_crypto_id_error():
        return ErrorMessages.errorMessages['cryptoIdError']

    @staticmethod
    def get_vs_currency_error():
        return ErrorMessages.errorMessages['vs_currencyError']

    @staticmethod
    def get_days_error():
        return ErrorMessages.errorMessages['daysError']
    
    @staticmethod
    def get_interval_error():
        return ErrorMessages.errorMessages['intervalError']
    
    @staticmethod
    def get_email_error():
        return ErrorMessages().errorMessages['emailError']
    
    @staticmethod
    def get_duplicate_email_error():
        return ErrorMessages().errorMessages['duplicateEmailError']
    
    @staticmethod
    def get_password_error():
        return ErrorMessages().errorMessages["passwordError"]

    @staticmethod
    def get_jwt_error():
        return ErrorMessages().errorMessages["jwtError"]

    @staticmethod
    def get_jwt_error():
        return ErrorMessages().errorMessages["jwtError"]

    @staticmethod
    def get_money_error():
        return ErrorMessages().errorMessages['moneyError']

    @staticmethod
    def get_negative_error():
        return ErrorMessages().errorMessages['negativeError']