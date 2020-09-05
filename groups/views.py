from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import (
    GroupBaseSerializer,
    confirmToGroupSerializer,
)

from .models import Group
from .permissions import groupConfirmMemberPermissions
from core.decode_jwt import request_get_user


class createAndShowGroupInfo(APIView):

    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        serializer = GroupBaseSerializer(Group.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupBaseSerializer(
            leader=request_get_user(request), data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)


class attendApplyToGroup(APIView):
    """
    그룹 참여 신청
    그룹 참여시 참가 신청 목록에 추가된다.
    """

    def get_object(self, pk):
        return Group.objects.get(pk=pk)

    def patch(self, request, pk):

        group = self.get_object(pk)
        user = request_get_user(request)
        group.attends.add(user)
        group.save()
        return Response("그룹에 참여하였습니다.", status=200)


class confirmMemberToGroup(APIView):
    """
    그룹 참가 승인
    그룹 참여시 참가 신청 목록에서 제거 후, 멤버로 등록한다.
    """

    permission_classes = [groupConfirmMemberPermissions]

    def get_object(self, pk):
        return Group.objects.get(pk=pk)

    def put(self, request, pk):
        groupObj = self.get_object(pk)
        serializer = confirmToGroupSerializer(group=groupObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
