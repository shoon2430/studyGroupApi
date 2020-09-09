import json
from pprint import pprint
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest_framework import status

from .models import Subject, Todo
from groups.models import Group
from users.models import User

from users.tests import userCreateSetUp


class SubejectCreateTestCase(userCreateSetUp):
    def setUp(self):
        super().setUp()
        data = {
            "category": "test",
            "title": "localhostGroup",
            "discription": "Hello my name ist local",
        }

        url = reverse("groups:groups")
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.post(url, data, format="json")

        self.group = Group.objects.get()

        data = {"title": "subjectTest"}
        url = reverse("todos:subjects", args=[self.group.pk])
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)["title"], "subjectTest")

    # 서브젝트 수정
    def test_update_subject(self):
        group = self.group
        subject = Subject.objects.get()
        leader = User.objects.get(username=self.user1["username"])
        member = User.objects.get(username=self.user2["username"])

        data = {"title": "Change_subjectTest"}
        url = reverse(
            "todos:subject-detail",
            kwargs={"group_pk": group.pk, "subject_pk": subject.pk},
        )

        # 해당그룹의 리더가 수정시
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["title"], "Change_subjectTest")

        # 그룹의 리더가 아닌 사람이 수정시
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content)["detail"], "그룹장만 승인이 가능합니다.")

    # 서브젝트 삭제
    def test_delete_subject(self):
        group = self.group
        subject = Subject.objects.get()
        leader = User.objects.get(username=self.user1["username"])
        member = User.objects.get(username=self.user2["username"])

        url = reverse(
            "todos:subject-detail",
            kwargs={"group_pk": group.pk, "subject_pk": subject.pk},
        )

        # 그룹의 리더가 아닌 사람이 삭제시
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 그룹의 리더가 삭제시
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # todo CRUD테스트
    def test_create_todo(self):
        group = self.group
        subject = Subject.objects.get()
        leader = User.objects.get(username=self.user1["username"])
        member = User.objects.get(username=self.user2["username"])

        # 그룹 참여요청 (맴버)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        url = reverse("groups:attend", args=[group.pk])
        response = self.client.patch(url, format="json")

        # 그룹 승인요청 (리더)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        url = reverse("groups:confirm", args=[group.pk])
        data = {"userId": member.username}
        response = self.client.patch(url, data, format="json")

        url = reverse(
            "todos:todos",
            kwargs={"subject_pk": subject.pk},
        )

        data = {"title": "todoTest"}
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)["title"], "todoTest")

        # todo 수정 및 삭제
        todo = Todo.objects.get()
        data = {"title": "ChangeTodoTest", "progress": "CREATE"}
        url = reverse(
            "todos:todo-detail",
            kwargs={"subject_pk": subject.pk, "todo_pk": todo.pk},
        )

        # 작성자가 아닌 사람이 수정시
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_2}")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["title"], "ChangeTodoTest")

        # 작성자가 삭제시
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.jwt_token_1}")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content)["detail"], "다른사람이 작성한 게시물은 수정할 수 었습니다."
        )
