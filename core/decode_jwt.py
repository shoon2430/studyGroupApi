import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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


def request_get_user(request):
    try:
        request_user_data = request_decode_jwt(request)
        if hasattr(request_user_data, "status_code"):
            if request_user_data.status_code != 200:
                return Response({"error_code": "AUTHORIZATION_NOT_FIND"}, status=401)

        return get_object_or_404(User, username=request_decode_jwt(request)["username"])

    except User.DoesNotExist:
        return Response({"error_code": "INVALID_TOKEN"}, status=401)