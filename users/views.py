import json
import jwt
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


class showUserApi(APIView):
    """
    유저 리스트 조회 API
    """

    # permission_classes = []
    # authentication_classes = ()

    def get(self, request):
        serializer = UserBaseSerializer(User.objects.all(), many=True)
        return Response(serializer.data)


class createUserApi(APIView):
    """
    회원가입 API
    """

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():

            if (
                User.objects.filter(
                    username=serializer.validated_data["username"]
                ).first()
                is None
            ):
                serializer.save()
                return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class updateUserApi(APIView):
    """
    회원정보 수정 API
    """

    # permission_classes = [IsAuthenticated]

    # authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self, username):
        return User.objects.get(username=username)

    def patch(self, request, username):
        user = self.get_object(username)
        serializer = UserUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid():

            serializer.update(instance=user, validated_data=request.data)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class deleteUserApi(APIView):
    """
    회원탈퇴
    """

    authentication_classes = [
        JSONWebTokenAuthentication,
    ]

    pass


class userLoginAPI(APIView):
    """
    로그인 API
    """

    permission_classes = []
    authentication_classes = ()

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class userLogoutAPI(APIView):
    """
    로그아웃
    """

    authentication_classes = [
        JSONWebTokenAuthentication,
    ]

    pass