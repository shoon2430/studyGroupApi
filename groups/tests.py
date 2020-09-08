import json
from pprint import pprint
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest_framework import status

from .models import Group
from users.models import User


class GroupCreateTestCase(APITestCase):
    def setUp(self):
        self.user1 = {
            "username": "local",
            "email": "test@local.host",
            "password": "1234",
            "nickname": "hoon",
            "phone": "",
            "introduce": "",
        }

        response = self.client.post(reverse("users:create"), self.user1, format="json")

        # 토큰추출
        data = {
            "username": self.user1["username"],
            "password": self.user1["password"],
        }
        response = self.client.post(reverse("users:get-token"), data, format="json")
        self.jwt_token = response.data["token"]

    # 그룹장이 그룹을 생성한다.
    def test_create_group(self):
        # 그룹 생성테스트
        url = reverse("groups:groups")
        data = {
            "category": "test",
            "title": "localhostGroup",
            "discription": "Hello my name ist local",
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token}")
        response = self.client.post(url, data, format="json")

        group = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(group["category"], data["category"])
        self.assertEqual(group["title"], data["title"])
        self.assertEqual(group["discription"], data["discription"])


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

        url = reverse("groups:groups")
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.post(url, self.group, format="json")

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

        # 그룹 참여요청 (맴버)
        url = reverse("groups:attend", args=[group.pk])
        response = self.client.patch(url, format="json")
        # 이미 참여신청 중이면 에러
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # 승인리스트에 추가되었는지 확인
        self.assertIn(member, group.attends.all())
        self.assertNotIn(member, group.members.all())

        # 그룹 승인요청 (리더)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        url = reverse("groups:confirm", args=[group.pk])
        data = {"userId": member.username}
        response = self.client.patch(url, data, format="json")

        # 맴버에 추가되었는지 확인
        self.assertIn(member, group.members.all())
        self.assertNotIn(member, group.attends.all())

        # 그룹 승인요청 (리더)
        url = reverse("groups:confirm", args=[group.pk])
        data = {"userId": leader.username}
        response = self.client.patch(url, data, format="json")

        # 이미 참여중이면 에러
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # 그룹 탈퇴 테스트
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        url = reverse("groups:out", args=[group.pk])
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(member, group.members.all())