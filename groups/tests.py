import json
from pprint import pprint
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest_framework import status

from .models import Group
from users.models import User


class GroupTestCase(APITestCase):
    def setUp(self):

        self.group = {
            "category": "test",
            "title": "localhostGroup",
            "discription": "Hello my name ist local",
        }

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

        # 초기화 동시에 유저 생성 테스트
        url = reverse("users:create")
        response = self.client.post(url, self.user1, format="json")
        response = self.client.post(url, self.user2, format="json")

        # 토큰추출
        url = reverse("users:get-token")
        data = {
            "username": self.user1["username"],
            "password": self.user1["password"],
        }
        response = self.client.post(url, data, format="json")
        self.jwt_token_1 = response.data["token"]
        data = {
            "username": self.user2["username"],
            "password": self.user2["password"],
        }
        response = self.client.post(url, data, format="json")
        self.jwt_token_2 = response.data["token"]

        # 그룹 생성테스트
        url = reverse("groups:info")
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.post(url, self.group, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().title, "localhostGroup")

    # 그룹 참여 테스트
    def test_join_group(self):
        group = Group.objects.get()

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        url = reverse("groups:attend", args=[group.pk])

        # 그룹 참여요청
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(group.attends.get().username, self.user2["username"])

    # 그룹 승인 테스트
    def test_confirm_group(self):
        group = Group.objects.get()
        leader = User.objects.get(username=self.user1["username"])
        member = User.objects.get(username=self.user2["username"])

        # 그룹 참여요청 (맴버)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        url = reverse("groups:attend", args=[group.pk])
        response = self.client.patch(url, format="json")

        # 승인리스트에 추가되었는지 확인
        self.assertIn(member, group.attends.all())
        self.assertNotIn(member, group.members.all())

        # 그룹 승인요청 (리더)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        url = reverse("groups:confirm", args=[group.pk])
        data = {"userId": member.username}
        response = self.client.put(url, data, format="json")

        # 맴버에 추가되었는지 확인
        self.assertIn(member, group.members.all())
        self.assertNotIn(member, group.attends.all())