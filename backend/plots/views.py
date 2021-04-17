from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import requests
import json
from classes.ErrorMessages import ErrorMessages
from classes.CryptoCurrency import CryptoCurrency

# Create your views here.
def plot(request, *args, **kwargs):
    if request.method != 'GET':
        return JsonResponse(ErrorMeesages.get_method_error())
    
    try:
        crypto = CryptoCurrency(kwargs['id'])
        return JsonResponse(crypto.get_prices(kwargs['vs_currency'], kwargs['days'], kwargs['interval']))
    except ValueError:
        return JsonResponse(ErrorMessages.get_crypto_id_error())

    


def plot_no_interval(request, *args, **kwargs):
    if request.method != 'GET':
        return JsonResponse(ErrorMeesages.get_method_error())

    try:
        crypto = CryptoCurrency(kwargs['id'])
        return JsonResponse(crypto.get_prices(kwargs['vs_currency'], kwargs['days']))
    except ValueError:
        return JsonResponse(ErrorMessages.get_crypto_id_error())

def cryptoList(request, *args, **kwargs):
    if request.method != 'GET':
        return JsonResponse(ErrorMessages.get_method_error())
    
    result = {
        "cryptoList": CryptoCurrency.cryptoIDs
    }
    return JsonResponse(result)