import json
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import (
    UserBaseSerializer,
    UserLoginSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)
from .models import User
from core.decode_jwt import request_get_user


class showUserApi(APIView):
    """
    유저 리스트 조회 API
    """

    permission_classes = []
    authentication_classes = ()

    def get(self, request):
        serializer = UserBaseSerializer(User.objects.all(), many=True)
        return Response(serializer.data)


class createUserApi(APIView):
    """
    회원가입 API
    """

    permission_classes = []
    authentication_classes = ()

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class updateUserApi(APIView):
    """
    회원정보 수정 API
    """

    def patch(self, request):
        user = request_get_user(request)
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=user, validated_data=request.data)
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


class deleteUserApi(APIView):
    """
    회원탈퇴
    """

    authentication_classes = [
        JSONWebTokenAuthentication,
    ]

    def delete(self, request):
        try:
            user = request_get_user(request)
            user.is_active = False
            user.save()
            return Response("회원탈퇴에 성공", status=200)
        except User.DoesNotExist:
            message = "존재하지 않는 유저입니다."
            return Response(message, status=200)


class userLoginAPI(APIView):
    """
    로그인 API
    """

    # 로그인 요청은 따로 인증이 필요없다고 판단
    permission_classes = []
    authentication_classes = ()

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)