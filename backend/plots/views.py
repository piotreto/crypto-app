from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import requests
import json

# Create your views here.
def plot(request, *args, **kwargs):


    if request.method != "GET":
        return JsonResponse()
    url = "https://api.coingecko.com/api/v3/coins/" + kwargs['id'] + "/market_chart?vs_currency=" + kwargs['vs_currency'] + "&days=" + kwargs['days'] + "&interval=" + kwargs['interval']
    data = requests.get(url).json()
    print(data['prices'])
    prices = {'prices': data['prices']}
    return JsonResponse(prices)
