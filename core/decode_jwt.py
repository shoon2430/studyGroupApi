import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response

from users.models import User


def decode_jwt(jwt_token):
    try:
        return jwt.decode(jwt_token, settings.SECRET_KEY, algorithm="HS256")
    except jwt.DecodeError:
        return Response({"error_code": "INVALID_TOKEN"}, status=401)


def request_decode_jwt(request):
    if "Authorization" not in request.headers:
        return Response({"error_code": "AUTHORIZATION_NOT_FIND"}, status=401)

    encode_token = request.headers["Authorization"].split(" ")[1]
    return decode_jwt(encode_token)
