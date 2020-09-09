import json
from pprint import pprint
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User
from .serializers import UserBaseSerializer

from core.decode_jwt import decode_jwt


class UserTestCase(APITestCase):
    def setUp(self):
        self.user1 = {
            "username": "local",
            "email": "test@local.host",
            "password": "1234",
            "nickname": "hoon",
            "phone": "",
            "introduce": "",
        }

        self.user2 = {
            "username": "host",
            "email": "host@local.host",
            "password": "1234",
            "nickname": "shoon",
            "phone": "",
            "introduce": "",
        }

        response = self.client.post(reverse("users:create"), self.user1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse("users:create"), self.user2, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 2)
        # 토큰추출
        data = {
            "username": self.user1["username"],
            "password": self.user1["password"],
        }
        response = self.client.post(reverse("users:get-token"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.jwt_token_1 = response.data["token"]

        data = {
            "username": self.user2["username"],
            "password": self.user2["password"],
        }
        response = self.client.post(reverse("users:get-token"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.jwt_token_2 = response.data["token"]

    # 유저 로그인 테스트
    def test_login_user(self):

        url = reverse("users:login")
        data = {"username": "local", "password": "1234"}

        # 로그인 요청
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 로그인 요청시 발급되는 토큰의 유저정보와 로그인요청한 유저의 정보가 같은지 확인
        token = response.data["token"]
        self.assertEqual(decode_jwt(token)["username"], "local")

    # 유저 회원정보 수정
    def test_modify_user(self):
        url = reverse("users:modify")
        data = {"nickname": "TEST", "email": "", "phone": "", "introduce": ""}

        # 토큰 세팅
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 변경된 값 비교
        user = User.objects.get(pk=decode_jwt(self.jwt_token_1)["user_id"])
        self.assertEqual(user.nickname, "TEST")

    # 유저 회원탈퇴
    def test_out_meneber_user(self):
        url = reverse("users:delete")
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")

        # 회원탈퇴 요청
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 변경된 유저 상태값 확인
        user = User.objects.get(pk=decode_jwt(self.jwt_token_1)["user_id"])
        self.assertEqual(user.is_active, False)


class userCreateSetUp(APITestCase):
    def setUp(self):
        self.user1 = {
            "username": "local",
            "email": "test@local.host",
            "password": "1234",
            "nickname": "hoon",
            "phone": "",
            "introduce": "",
        }

        self.user2 = {
            "username": "host",
            "email": "host@local.host",
            "password": "1234",
            "nickname": "shoon",
            "phone": "",
            "introduce": "",
        }

        response = self.client.post(reverse("users:create"), self.user1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse("users:create"), self.user2, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 2)
        # 토큰추출
        data = {
            "username": self.user1["username"],
            "password": self.user1["password"],
        }
        response = self.client.post(reverse("users:get-token"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.jwt_token_1 = response.data["token"]

        data = {
            "username": self.user2["username"],
            "password": self.user2["password"],
        }
        response = self.client.post(reverse("users:get-token"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.jwt_token_2 = response.data["token"]