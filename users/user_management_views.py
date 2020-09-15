import json
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from todos.models import Subject, Todo, TodoGroup
from core.decode_jwt import request_get_user

from .user_management_serializers import myGroupInnerTodoSerializer, DeviceSerializer
from groups.serializers import GroupBaseSerializer
from todos.serializers import todoAllSerializer

"""
자기 자신이 속한 그룹의 정보
todo 정보 조회
"""


class userInnerGroupsApi(APIView):
    """
    내가 속한 그룹들 보기
    """

    def get(self, request):
        user = request_get_user(request)
        group = user.attendGroups.all()
        serializer = GroupBaseSerializer(group, many=True)
        return Response(serializer.data)


# 그룹과 todo를 함께 담기위한 클래스
class groupAndTodoDevice(object):
    def __init__(self, group, todos):
        self.group = group
        self.todos = todos


class userInnerTodosApi(APIView):
    """
    내가 해야할 투두 보기
    """

    def get(self, request):
        #  유저를 받아온다 hoon
        user = request_get_user(request)
        # hoon이 속한 그룹을 가져온다
        groups = user.attendGroups.all()

        devices = []
        for group in groups:
            subjects = Subject.objects.filter(group_id=group)
            todoGroups = TodoGroup.objects.filter(subject_id__in=subjects)
            todos = Todo.objects.filter(todoGroup_id__in=todoGroups, writer=user)
            devices.append(groupAndTodoDevice(group, todos))

        serializer = DeviceSerializer(devices, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(status=500)
