import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest_framework import status

from .models import Group
from users.models import User


# class GroupTestCase(APITestCase):
#     def setUp(self):

#         group = {
#             "category": "cate1",
#             "title": "localhost1",
#             "discription": "Hello my name ist local",
#         }

#         user1 = {
#             "username": "local",
#             "email": "test@local.host",
#             "password": "1234",
#             "name": "hoon",
#         }
#         user2 = {
#             "username": "callo",
#             "email": "test@local.host",
#             "password": "1234",
#             "name": "jsh",
#         }

#         url = reverse("users:create")
#         response = self.client.post(url, user1, format="json")
#         response = self.client.post(url, user2, format="json")

#         self.leader = User.objects.get(username="local")
#         self.member = User.objects.get(username="callo")

#         url = reverse("groups:list")
#         data = group

#         self.client.force_authenticate(self.leader)
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     # 그룹 생성테스트
#     def test_create_user(self):

#         self.assertEqual(Group.objects.count(), 1)
#         self.assertEqual(Group.objects.get().title, "localhost1")

#     # 그룹 참여 테스트
#     def test_join_group(self):
#         group = Group.objects.get()
#         member = self.member

#         self.client.force_authenticate(member)
#         url = reverse("groups:attend", args=[group.pk])
#         # data = {"userId": "local2"}
#         # response = self.client.put(url, data, format="json")

#         data = {"userId": member.username}
#         response = self.client.put(url, data, format="json")

#         self.assertIn(member, Group.objects.get().attends.all())

#     # 그룹 승인 테스트
#     def test_confirm_group(self):
#         group = Group.objects.get()
#         leader = self.leader
#         member = self.member

#         self.client.force_authenticate(member)

#         url = reverse("groups:attend", args=[group.pk])
#         data = {"userId": member.username}
#         response = self.client.put(url, data, format="json")

#         self.assertIn(member, Group.objects.get().attends.all())
#         self.assertNotIn(member, Group.objects.get().members.all())

#         self.client.force_authenticate(leader)
#         url = reverse("groups:confirm", args=[group.pk])
#         data = {"userId": member.username}
#         response = self.client.put(url, data, format="json")

#         self.assertIn(member, Group.objects.get().members.all())
#         self.assertNotIn(member, Group.objects.get().attends.all())