import json
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from users.models import User
from groups.models import Group
from core.decode_jwt import request_get_user


class MyException(Exception):
    pass


class groupConfirmMemberPermissions(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        try:
            isCheck = False
            user = request_get_user(request)
            if user:
                isCheck = True
                pk = view.kwargs["pk"]
                group = get_object_or_404(Group, pk=pk)
                if group.leader != user:
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