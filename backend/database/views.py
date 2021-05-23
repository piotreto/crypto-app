from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
import requests
import json
import jwt
from classes.ErrorMessages import ErrorMessages
from classes.CryptoCurrency import CryptoCurrency
from database.models import User
from .database_validators import *
from django.contrib.auth.hashers import make_password, check_password

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
    amount = float(kwargs['amount'].replace("a", "."))

    if (amount < 0):
        return JsonResponse(ErrorMessages.get_negative_error(), status=400)
        
    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']

    if not checkIfWalletExists(user_email, crypto.id):
        return JsonResponse(ErrorMessages.get_money_error(), status=400)

    if not checkIfUserHasEnoughCurrency(user_email, amount, crypto.id):
        return JsonResponse(ErrorMessages.get_money_error(), status=400)

    sellValue = crypto.get_single_value() * amount
    
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
    amount = float(kwargs['amount'].replace("a", "."))

    if (amount < 0):
        return JsonResponse(ErrorMessages.get_negative_error(), status=400)

    user_email = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])['email']
    
    user = User.objects.get(email = user_email)

    if not checkIfUserHasEnoughCurrency(user_email, amount, 'usd'):
        return JsonResponse(ErrorMessages.get_money_error(), status=400)
    
    buyValue = (1/crypto.get_single_value()) * amount

    if not checkIfWalletExists(user_email, crypto.id):
        wallet = Wallet(user = user, cryptoID = crypto.id, amount = buyValue)
        wallet.save()
    else:
        wallet = Wallet.objects.get(user = user, cryptoID = crypto.id)
        wallet.amount += buyValue
        wallet.save()
    
    user.dollars -= amount
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






    
