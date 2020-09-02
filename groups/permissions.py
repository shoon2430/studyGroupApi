import json
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from users.models import User
from django.shortcuts import get_object_or_404


class MyException(Exception):
    pass


class groupJoinPermissions(BasePermission):
    def has_permission(self, request, view):
        isCheck = True
        isCheck = request.user and request.user.is_authenticated

        try:
            if request.body:
                userId = json.loads(request.body)["userId"]
                user = get_object_or_404(User, username=userId)

                if user.pk != request.user.pk:
                    raise MyException("자기 자신만 가입이 가능합니다.")
                    isCheck = False
            else:
                isCheck = False

        except User.DoesNotExist:
            isCheck = False

        return isCheck