import json
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from todos.models import Subject, Todo, TodoGroup
from core.decode_jwt import request_get_user

from groups.serializers import GroupBaseSerializer
from .user_management_serializers import myGroupInnerTodoSerializer

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


# class userInnerTodosApi(APIView):
#     """
#     내가 해야할 투두 보기
#     """

#     def get(self, request):
#         #  유저를 받아온다 hoon
#         user = request_get_user(request)
#         # hoon이 속한 그룹을 가져온다
#         group = user.attendGroups.all()
#         # 이그룹에 해당하는 todo중 내가 해야하는 것만 보고싶다
#         serializer = myGroupInnerTodoSerializer(group, user, many=True)
#         return Response(serializer.data)