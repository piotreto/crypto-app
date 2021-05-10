from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
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
        return JsonResponse(ErrorMessages.get_method_error())

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    email = body['email']
    password = body['password']

    if not validateEmail(email):
        return JsonResponse(ErrorMessages.get_email_error())
    
    if checkIfUserExists(email):
        return JsonResponse(ErrorMessages.get_duplicate_email_error())
    
    user = User(email = email, password = make_password(password))
    user.save()

    return JsonResponse({
        "error": 0
    })

def login(request, *arg, **kwargs):
    if request.method != 'POST':
        return JsonResponse(ErrorMessages.get_method_error())

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    email = body['email']
    password = body['password']

    if not checkIfUserExists(email):
        return JsonResponse(ErrorMessages.get_email_error())
    
    if not checkIfPasswordMatches(email, password):
        return JsonResponse(ErrorMessages().get_password_error())

    encoded_jwt = jwt.encode({"email": email}, "SECRET", algorithm="HS256")
    result = {
        "JWT": encoded_jwt
    }

    return JsonResponse(result)

