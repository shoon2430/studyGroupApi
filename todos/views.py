import json
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import (
    SubjectSimpleSerializer,
    SubjectBaseSerializer,
    groupSubjectsSerializer,
    SubjectDetailSerializer,
    todoGroupSimpleSerializer,
    todoGroupDetailSerializer,
    todoSimpleSerializer,
    todoDetailSerializer,
)

from .permissions import (
    myGroupOnlyToSubjectPermissions,
    myGroupOnlyToTodoPermissions,
    todoDetailPermissions,
)

from .models import Subject, Todo, TodoGroup
from users.models import User
from groups.models import Group
from core.decode_jwt import request_get_user

from pprint import pprint


class subjectCreateApi(APIView):
    """
    subject 생성
    """

    permission_classes = []
    authentication_classes = ()

    def get_object(self, group_pk):
        group = get_object_or_404(Group, pk=group_pk)
        return Subject.objects.filter(group_id=group)

    def get(self, request, group_pk):
        subjects = self.get_object(group_pk)
        serializer = SubjectSimpleSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request, group_pk):
        serializer = SubjectBaseSerializer(
            group=get_object_or_404(Group, pk=group_pk),
            leader=request_get_user(request),
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)


class subjectDetailApi(APIView):
    """
    Subject 상세 정보 보기
    """

    permission_classes = [
        myGroupOnlyToSubjectPermissions,
    ]

    def get(self, request, group_pk, subject_pk):
        subject = get_object_or_404(Subject, pk=subject_pk)
        serializer = SubjectSimpleSerializer(subject)
        return Response(serializer.data)

    def patch(self, request, group_pk, subject_pk):
        user = request_get_user(request)
        group = (get_object_or_404(Group, pk=group_pk),)

        serializer = SubjectDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(
                get_object_or_404(Subject, pk=subject_pk), serializer.data
            )
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, group_pk, subject_pk):
        subject = get_object_or_404(Subject, pk=subject_pk)
        subject.delete()
        return Response("subject가 삭제되었습니다.", status=200)


class todoGroupCreateApi(APIView):
    """
    todoGroup 생성
    """

    permission_classes = [
        myGroupOnlyToTodoPermissions,
    ]

    def post(self, request, subject_pk):
        serializer = todoGroupSimpleSerializer(
            subject=get_object_or_404(Subject, pk=subject_pk),
            writer=request_get_user(request),
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)


class todoGroupDetailApi(APIView):
    def patch(self, request, subject_pk, todoGoup_pk):

        serializer = todoGroupDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(
                get_object_or_404(TodoGroup, pk=todoGoup_pk), serializer.data
            )
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, subject_pk, todoGoup_pk):
        todo = get_object_or_404(TodoGroup, pk=todoGoup_pk)
        todo.delete()
        return Response("subject가 삭제되었습니다.", status=200)


class addUserFromTodoGroupApi(APIView):
    """
    만들어진 todoGroup에 그룹원들 추가하기
    """

    def post(self, request, subject_pk, todoGoup_pk):
        userIds = json.loads(request.body)["users"]

        # 요청을 정상적으로 한 경우
        if userIds:
            users = User.objects.filter(username__in=userIds)
            # 유효한 유저가 한명이라도 있을경우
            if len(users) > 0:
                todoGroup = get_object_or_404(TodoGroup, pk=todoGoup_pk)
                for user in users:
                    # todoGroup에 유저를 추가 후
                    todoGroup.members.add(user)
                    # 해당되는 유저의 todo를 생성해준다.
                    Todo.objects.create(
                        todoGroup_id=todoGroup,
                        time=todoGroup.time,
                        title=todoGroup.title,
                        progress=todoGroup.progress,
                        writer=user,
                    )

                todoGroup.save()
                return Response("그룹원 추가 완료", status=200)
            else:
                return Response("유저 정보가 올바르지 않습니다.", status=400)
        else:
            return Response("해당 요청이 잘못되었습니다.", status=400)


class todoDetailApi(APIView):
    pass