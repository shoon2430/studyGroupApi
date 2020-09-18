from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import (
    GroupBaseSerializer,
    GroupInfoShowSerializer,
    GroupInfoUpdateSerializer,
)

from users.models import User
from .models import Group
from .permissions import groupConfirmMemberPermissions
from core.decode_jwt import request_get_user


class createAndShowGroupInfoApi(APIView):
    """
    그룹 전체 조회 및 그룹 생성
    """

    permission_classes = []
    authentication_classes = ()

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


class groupDetailApi(APIView):
    """
    그룹 상세 정보 조회
    그룹에 해당하는 subject들을 보여준다

    그룹 상세정보 수정 및 삭제
    """

    permission_classes = []
    authentication_classes = ()

    def get_object(self, pk):
        return get_object_or_404(Group, pk=pk)

    def get(self, request, pk):
        serializer = GroupInfoShowSerializer(self.get_object(pk))
        return Response(serializer.data)

    def patch(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupInfoUpdateSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        group = self.get_object(pk)
        group.delete()
        return Response("그룹이 삭제되었습니다.", status=200)


class attendApplyToGroupApi(APIView):
    """
    그룹 참여 신청
    그룹 참여시 참가 신청 목록에 추가된다.
    """

    def get_object(self, pk):
        return Group.objects.get(pk=pk)

    def put(self, request, pk):

        group = self.get_object(pk)
        user = request_get_user(request)

        # 참가신청목록과, 그룹멤버에 포함되지 않아야 신청가능하다.
        if user in group.attends.all():
            return Response("이미 참가신청을 하였습니다.", status=405)
        elif user in group.members.all():
            return Response("이미 그룹에 참여중입니다.", status=405)

        group.attends.add(user)
        group.save()
        return Response("참가신청 되었습니다.", status=200)


class confirmMemberToGroupApi(APIView):
    """
    그룹 참가 승인
    그룹 참여시 참가 신청 목록에서 제거 후, 멤버로 등록한다.
    """

    permission_classes = [groupConfirmMemberPermissions]

    def get_object(self, pk):
        return Group.objects.get(pk=pk)

    def put(self, request, pk):
        group = self.get_object(pk)
        print(group)
        userIdList = request.data["userIdList"]

        if userIdList:
            userList = []
            for userId in userIdList:
                user = User.objects.get(pk=userId)

                if user not in group.attends.all():
                    return Response("참가신청을 하지 않은 유저입니다.", status=405)

                if user in group.members.all():
                    return Response("이미 그룹에 참여중인 유저입니다.", status=405)
                userList.append(user)

            for user in userList:
                group.attends.remove(user)
                group.members.add(user)

                # 유저 정보에 그룹 정보 추가
                user.attendGroups.add(group)
                user.save()

            group.save()
            return Response("승인 되었습니다.", status=200)
        else:
            return Response("잘못된 요청입니다.", status=400)


class outApplyToGroupApi(APIView):
    """
    그룹 탈퇴
    """

    def get_object(self, pk):
        return Group.objects.get(pk=pk)

    def delete(self, request, pk):

        group = self.get_object(pk)
        user = request_get_user(request)

        # 참가신청목록과, 그룹멤버에 포함되지 않아야 신청가능하다.
        if user in group.attends.all():
            group.attends.remove(user)
            group.save()
            return Response("참가신청이 취소 되었습니다.", status=200)
        elif user in group.members.all():
            group.members.remove(user)
            user.attendGroups.remove(group)
            user.save()
            group.save()
            return Response("그룹에서 탈퇴하였습니다.", status=200)
        else:
            return Response("해당 그룹에 속한 정보가 없습니다.", status=405)