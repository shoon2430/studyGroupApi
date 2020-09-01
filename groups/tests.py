import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Group
from users.models import User


class GroupTestCase(APITestCase):
    def setUp(self):
        self.user1 = {
            "username": "test1",
            "email": "test@local.host",
            "password": "1234",
            "name": "jsh",
        }
        self.group1 = {
            "photo": "testUrl",
            "category": "local",
            "title": "localhost1",
            "discription": "Hello my name ist local",
            "leader": "hoon",
            "time": "1",
        }
        self.group2 = {
            "photo": "testUrl2",
            "category": "local2",
            "title": "localhost2",
            "discription": "Hello my name ist local22",
            "leader": "soon",
            "time": "2",
        }

    def test_create_user(self):
        url = reverse("users:create")
        data = self.user1
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, "jsh")


