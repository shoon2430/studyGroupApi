import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User
from .serializers import UserCreateSerializer


class ModelTestCase(APITestCase):
    def setUp(self):
        self.user1 = {
            "username": "test1",
            "email": "test@local.host",
            "password": "1234",
            "name": "jsh",
        }

        self.user2 = {
            "username": "test1",
            "email": "test@local.host",
            "password": "1234",
            "name": "jsh",
        }

    def test_create_user(self):
        url = reverse("users:create")
        data = self.user1
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, "jsh")
