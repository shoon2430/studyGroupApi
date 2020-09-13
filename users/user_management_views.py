import json
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from core.decode_jwt import request_get_user

from groups.serializers import GroupBaseSerializer

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
        group = user.attendGroups
        serializer = GroupBaseSerializer(group, many=True)
        return Response(serializer.data)
