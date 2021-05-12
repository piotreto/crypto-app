from database.models import User, Wallet
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.hashers import make_password, check_password

def checkIfUserExists(user_name):
    return User.objects.filter(email = user_name).exists()
    

def checkIfPasswordMatches(user_name, user_password):
    user = User.objects.get(email = user_name)
    return check_password(user_password, user.password)

def validateEmail(email="sedziborow..$$"):
    try:
        valid = validate_email(email)
        return True

    except EmailNotValidError:
        return False
        
def checkIfUserHasEnoughCurrency(user_name, amount, currency_name):
    user = User.objects.get(email = user_name)
    if currency_name == 'usd':
        if user.dollars < amount:
            return False
        else:
            return True
    else:
        wallet = Wallet.objects.get(user = user, cryptoID = currency_name)
        if wallet.amount < amount:
            return False
        else:
            return True
            
def checkIfWalletExists(user_name, crypto_id):
    user = User.objects.get(email = user_name)
    if Wallet.objects.filter(user = user, cryptoID = crypto_id).exists():
        return True
    else:
        return False
        
    

    