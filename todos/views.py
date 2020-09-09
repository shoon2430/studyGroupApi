from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import (
    SubjectSimpleSerializer,
    SubjectBaseSerializer,
    groupSubjectsSerializer,
    SubjectDetailSerializer,
)

from .permissions import subjectDetailPermissions

from .models import Subject, Todo
from groups.models import Group
from core.decode_jwt import request_get_user


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
    permission_classes = [
        subjectDetailPermissions,
    ]

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