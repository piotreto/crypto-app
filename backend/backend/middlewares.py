import jwt
import json
from base64 import b64decode
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from classes.ErrorMessages import ErrorMessages

class jwtMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.views = ['sell', 'buy']

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__name__ not in self.views:
            return view_func(request, *view_args, **view_kwargs)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if 'jwt' not in body:
            return JsonResponse(ErrorMessages.get_jwt_error())

        encoded_jwt = body['jwt']
        try:
            payload = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            return JsonResponse(ErrorMessages.get_jwt_error())

        if jwt.encode(payload, "SECRET", algorithm='HS256') == encoded_jwt:
            return None

        return JsonResponse(ErrorMessages.get_jwt_error())
        

class jwtMiddlewareWrapper(jwtMiddleware, MiddlewareMixin):
    pass