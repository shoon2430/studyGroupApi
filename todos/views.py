from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import (
    SubjectSimpleSerializer,
    SubjectBaseSerializer,
    groupSubjectsSerializer,
    SubjectDetailSerializer,
    todoSimpleSerializer,
    todoDetailSerializer,
)

from .permissions import (
    myGroupOnlyToSubjectPermissions,
    myGroupOnlyToTodoPermissions,
    todoDetailPermissions,
)

from .models import Subject, Todo
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


class todoCreateApi(APIView):
    """
    todo 생성
    """

    permission_classes = [
        myGroupOnlyToTodoPermissions,
    ]

    def post(self, request, subject_pk):
        serializer = todoSimpleSerializer(
            subject=get_object_or_404(Subject, pk=subject_pk),
            writer=request_get_user(request),
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)


class todoDetailApi(APIView):
    permission_classes = [
        todoDetailPermissions,
    ]

    def patch(self, request, subject_pk, todo_pk):

        serializer = todoDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(get_object_or_404(Todo, pk=todo_pk), serializer.data)
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, subject_pk, todo_pk):
        todo = get_object_or_404(Todo, pk=todo_pk)
        todo.delete()
        return Response("subject가 삭제되었습니다.", status=200)