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
            "username": "local",
            "email": "test@local.host",
            "password": "1234",
            "name": "jsh",
        }
        url = reverse("users:create")
        data = self.user
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 유저 생성 테스트
    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, "jsh")
