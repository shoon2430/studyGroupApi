import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User
from .serializers import UserBaseSerializer


class ModelTestCase(APITestCase):
    def setUp(self):
        self.user = {
            "username": "local2",
            "email": "test@local.host",
            "password": "1234",
            "nickname": "jsh",
        }

        # 초기화 동시에 유저 생성 테스트
        url = reverse("users:create")
        data = self.user
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    # 유저 로그인 테스트
    def test_login_user(self):

        data = {"username": "local2", "password": "1234"}
        url = reverse("users:login")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = response.data["token"]
        print(token)

    def test_logout_user(self):
        print(self.token)
        self.assertEqual(User.objects.count(), 1)