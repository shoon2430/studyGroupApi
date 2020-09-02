import json
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from users.models import User
from groups.models import Group


class MyException(Exception):
    pass


class groupAttendApplyPermissions(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        isCheck = request.user and request.user.is_authenticated

        try:
            if request.body:
                userId = json.loads(request.body)["userId"]
                user = get_object_or_404(User, username=userId)

                if user.pk != request.user.pk:
                    self.message = "자기 자신만 신청이 가능합니다."
                    isCheck = False
            else:
                isCheck = False

        except User.DoesNotExist:
            self.message = "존재하지 않는 유저입니다."
            isCheck = False

        return isCheck


class groupConfirmMemberPermissions(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        isCheck = request.user and request.user.is_authenticated

        try:
            if request.body:
                pk = view.kwargs["pk"]
                group = get_object_or_404(Group, pk=pk)
                if group.leader != request.user:
                    self.message = "그룹장만 승인이 가능합니다."
                    isCheck = False
            else:
                isCheck = False
        except User.DoesNotExist:
            self.message = "존재하지 않는 유저입니다."
            isCheck = False
        except Group.DoesNotExist:
            self.message = "존재하지 않는 그룹입니다."
            isCheck = False

        return isCheck