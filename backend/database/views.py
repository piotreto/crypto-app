from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
import requests
import json
import jwt
from classes.ErrorMessages import ErrorMessages
from classes.CryptoCurrency import CryptoCurrency
from database.models import User, Wallet, TradeHistory
from .database_validators import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

def register(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    email = body['email']
    password = body['password']
    dollars = 1000

    if not validateEmail(email):
        return JsonResponse(ErrorMessages.get_email_error(), status=400)
    
    if checkIfUserExists(email):
        return JsonResponse(ErrorMessages.get_duplicate_email_error(), status=400)
    
    user = User(email = email, password = make_password(password), dollars = dollars)
    user.save()

    return JsonResponse({
        "error": 0
    })

def login(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    email = body['email']
    password = body['password']

    if not checkIfUserExists(email):
        return JsonResponse(ErrorMessages.get_email_error(), status=400)
    
    if not checkIfPasswordMatches(email, password):

        return JsonResponse(ErrorMessages().get_password_error(), status=400)

    encoded_jwt = jwt.encode({"email": email}, "SECRET", algorithm="HS256")
    result = {
        "JWT": encoded_jwt,
        "email": email
    }

    return JsonResponse(result)

# JWT MiddleWare
def sell(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    encoded_jwt = body['JWT']
    crypto = CryptoCurrency(kwargs['id'])

    #amount of crypto we wanna sell
    amount = float(kwargs['amount'].replace("a", "."))

    if (amount < 0):
        return JsonResponse(ErrorMessages.get_negative_error(), status=400)
        
    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']
    user = User.objects.get(email = user_email)

    if not checkIfWalletExists(user_email, crypto.id):
        return JsonResponse(ErrorMessages.get_money_error(), status=400)

    if not checkIfUserHasEnoughCurrency(user_email, amount, crypto.id):
        return JsonResponse(ErrorMessages.get_money_error(), status=400)
        
    
    price = crypto.get_single_value()
    sellValue = price * amount

    trade_history = TradeHistory(user=user, cryptoID=crypto.id, amount=amount, tradeDate= timezone.now(), tradeType="SELL", currentPrice = price)
    trade_history.save()
    
    user = User.objects.get(email = user_email)
    user.dollars += sellValue
    user.save()

    wallet = Wallet.objects.get(user = user, cryptoID = kwargs['id'])
    wallet.amount -= amount
    wallet.save()

    return JsonResponse({"error": 0})

# JWT MiddleWare
def buy(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    encoded_jwt = body['JWT']
    crypto = CryptoCurrency(kwargs['id'])
    
    #amount of crypto we wanna buy
    buyValue = float(kwargs['amount'].replace("a", "."))

    if (buyValue < 0):
        return JsonResponse(ErrorMessages.get_negative_error(), status=400)

    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']
    
    user = User.objects.get(email = user_email)

    if not checkIfUserHasEnoughCurrency(user_email, buyValue, 'usd'):
        return JsonResponse(ErrorMessages.get_money_error(), status=400)
    
    price = crypto.get_single_value()
    amount = (1/price) * buyValue

    trade_history = TradeHistory(user=user, cryptoID=crypto.id, amount=amount, tradeDate= timezone.now(), tradeType="BUY", currentPrice=price)
    trade_history.save()

    if not checkIfWalletExists(user_email, crypto.id):
        wallet = Wallet(user = user, cryptoID = crypto.id, amount = amount)
        wallet.save()
    else:
        wallet = Wallet.objects.get(user = user, cryptoID = crypto.id)
        wallet.amount += amount
        wallet.save()
    
    user.dollars -= buyValue
    user.save()
    
    return JsonResponse({"error": 0}, status=200)

# JWT MiddleWare
def wallet_details(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    encoded_jwt = body['JWT']
    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']

    user = User.objects.get(email = user_email)
    wallet = Wallet.objects.filter(user = user)
    wallet = list(map(lambda wallet: {"cryptoID": wallet.cryptoID, "amount": wallet.amount}, wallet))

    result = {}
    result['dollars'] = user.dollars
    result['wallet_info'] = wallet
    return JsonResponse(result)
    
def trades_history(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)
        
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    encoded_jwt = body['JWT']
    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']

    user = User.objects.get(email = user_email)
    history = TradeHistory.objects.filter(user=user).order_by('-tradeDate')
    history = list(map(lambda trade: {
        "cryptoID": trade.cryptoID, 
        "amount": trade.amount, 
        "dateTrade": trade.tradeDate, 
        "type": trade.tradeType, 
        "currentPrice": trade.currentPrice
        }, history))

    result = {}
    result['trades'] = history
    return JsonResponse(result)

def daily_crypto_statistics(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    encoded_jwt = body['JWT']
    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']

    user = User.objects.get(email = user_email)
    wallet = Wallet.objects.filter(user = user)

    stats_list = []
    for obj in wallet:
        crypto = CryptoCurrency(obj.cryptoID)
        today_price = crypto.get_single_value()
        yesterday_price = crypto.get_previous_day_price()
        percentage = 100 * (today_price - yesterday_price) / yesterday_price
        stats_list.append({"cryptoID": crypto.id, "percentage": percentage})

    result = {}
    result["stats"] = stats_list

    return JsonResponse(result)

def daily_statistics(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error(), status=400)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    encoded_jwt = body['JWT']
    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']

    user = User.objects.get(email = user_email)
    previous_day = get_previous_day_sum(user_email)
    current_day = get_current_day_sum(user_email)

    result = {}
    result['percentage'] = (current_day - previous_day)/previous_day * 100
    result['difference'] = current_day - previous_day
    
    return JsonResponse(result)
    

def get_current_day_sum(user_email):
    user = User.objects.get(email=user_email)
    wallet = Wallet.objects.filter(user = user)
    result = user.dollars

    for balance in wallet:
        crypto = CryptoCurrency(balance.cryptoID)
        result += balance.amount * crypto.get_single_value()
    
    return result

def get_previous_day_sum(user_email):
    user = User.objects.get(email=user_email)
    wallet = Wallet.objects.filter(user = user)
    result = user.dollars

    for balance in wallet:
        previous_price = get_previous_day_price(balance.cryptoID)
        result += get_previous_day_price(balance.cryptoID) * balance.amount

    return result




    

    
    






    
