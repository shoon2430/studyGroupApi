import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User
from .serializers import UserCreateSerializer


class ModelTestCase(APITestCase):
    def test_setup(self):
        user = User.objects.create(
            username="test",
            email="test@localhost.app",
            password="1234",
            name="man",
        )

    def test_create_user(self):
        url = reverse("users:create")

        data = {
            "username": "test",
            "email": "test@localhost.app",
            "password": "1234",
            "name": "man",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="test")
        self.assertEqual(user.password, "1234")
