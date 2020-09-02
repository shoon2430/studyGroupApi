import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest_framework import status

from .models import Group
from users.models import User


class GroupTestCase(APITestCase):
    def setUp(self):

        group = {
            "category": "local",
            "title": "localhost1",
            "discription": "Hello my name ist local",
            "leader_id": "1",
            "time": "1",
        }

        user1 = {
            "username": "local2",
            "email": "test@local.host",
            "password": "1234",
            "name": "jsh",
        }
        user2 = {
            "username": "local3",
            "email": "test@local.host",
            "password": "1234",
            "name": "jsh",
        }

        url = reverse("users:create")
        response = self.client.post(url, user1, format="json")
        response = self.client.post(url, user2, format="json")

        url = reverse("groups:all-list")
        data = group
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user(self):
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().title, "localhost1")

    def test_join_group(self):
        user = User.objects.get(id=2)

        self.client.force_authenticate(user)
        url = reverse("groups:update", args=[1])
        # data = {"userId": "local2"}
        # response = self.client.put(url, data, format="json")

        data = {"userId": user.username}
        response = self.client.put(url, data, format="json")