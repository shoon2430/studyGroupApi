import json
from pprint import pprint
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User
from .serializers import UserBaseSerializer

from core.decode_jwt import decode_jwt


class ModelTestCase(APITestCase):
    def setUp(self):
        self.user = {
            "username": "local",
            "email": "test@local.host",
            "password": "1234",
            "nickname": "hoon",
            "phone": "",
            "introduce": "",
        }

        # 초기화 동시에 유저 생성 테스트
        url = reverse("users:create")
        data = self.user
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        # 토큰추출

        url = reverse("users:get-token")
        data = {"username": "local", "password": "1234"}
        response = self.client.post(url, data, format="json")

        self.jwt_token = response.data["token"]
        self.assertIsNotNone(response.data["token"])

    # 유저 로그인 테스트
    def test_login_user(self):

        data = {"username": "local", "password": "1234"}
        url = reverse("users:login")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = response.data["token"]

        self.assertEqual(decode_jwt(token)["username"], "local")

    # 유저 회원정보 수정
    def test_modify_user(self):
        url = reverse("users:modify", args=[self.user["username"]])
        data = {"nickname": "TEST", "email": "", "phone": "", "introduce": ""}

        # 토큰 세팅
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token}")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 변경된 값 비교
        user = User.objects.get(pk=decode_jwt(self.jwt_token)["user_id"])
        self.assertEqual(user.nickname, "TEST")

    # 유저 회원탈퇴
    # def test_out_meneber_user(self):
    #     pass