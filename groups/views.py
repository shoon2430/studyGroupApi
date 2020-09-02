from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    GroupBaseSerializer,
    attendToGroupSerializer,
    confirmToGroupSerializer,
)

from .models import Group
from .permissions import groupAttendApplyPermissions, groupConfirmMemberPermissions


class createAndShowGroupInfo(APIView):
    def get(self, request):
        serializer = GroupBaseSerializer(Group.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupBaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)


class attendApplyToGroup(APIView):
    """
    그룹 참여 신청
    그룹 참여시 참가 신청 목록에 추가된다.

    로그인이 되어있어야하고, 자기 자신만 신청할 수 있다.
    """

    permission_classes = [groupAttendApplyPermissions]

    def get_object(self, pk):
        return Group.objects.get(pk=pk)

    def put(self, request, pk):
        groupObj = self.get_object(pk)
        serializer = attendToGroupSerializer(group=groupObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)


class confirmMemberToGroup(APIView):
    """
    그룹 참가 승인
    그룹 참여시 참가 신청 목록에서 제거 후, 멤버로 등록한다.

    로그인이 되어있어야하고, 자기 자신만 신청할 수 있다.
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
