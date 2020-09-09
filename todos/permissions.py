import json
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .models import Subject, Todo
from users.models import User
from groups.models import Group
from core.decode_jwt import request_get_user


class myGroupOnlyToSubjectPermissions(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        try:
            isCheck = False
            user = request_get_user(request)
            if user:
                isCheck = True
                pk = view.kwargs["group_pk"]
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


# 자신이 속한 그룹에서만 작성 가능
class myGroupOnlyToTodoPermissions(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        try:
            isCheck = False
            user = request_get_user(request)
            if user:
                isCheck = True
                subject_pk = view.kwargs["subject_pk"]
                subject = get_object_or_404(Subject, pk=subject_pk)

                # 해당 유저가 속한 그룹의 Subject가 아닌경우
                if subject.group_id not in user.attendGroups.all():
                    self.message = "자신이 속한 그룹에서만 작성 가능합니다."
                    isCheck = False
            else:
                isCheck = False
        except User.DoesNotExist:
            self.message = "존재하지 않는 유저입니다."
            isCheck = False
        except Subject.DoesNotExist:
            self.message = "존재하지 않는 목표입니다."
            isCheck = False

        return isCheck


# 자신이 작성한 글만 수정 삭제 가능
class todoDetailPermissions(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        try:
            isCheck = False
            user = request_get_user(request)
            if user:
                isCheck = True

                subject_pk = view.kwargs["subject_pk"]
                todo_pk = view.kwargs["todo_pk"]
                subject = get_object_or_404(Subject, pk=subject_pk)
                todo = get_object_or_404(Todo, pk=todo_pk)

                # 해당 유저가 속한 그룹의 Subject가 아닌경우
                if subject.group_id not in user.attendGroups.all():
                    self.message = "다른사람이 작성한 게시물은 수정할 수 었습니다."
                    isCheck = False

                # 내가 작성한 글이 아닌 경우
                if todo.writer != user:
                    self.message = "다른사람이 작성한 게시물은 수정할 수 었습니다."
                    isCheck = False
            else:
                isCheck = False
        except User.DoesNotExist:
            self.message = "존재하지 않는 유저입니다."
            isCheck = False
        except Subject.DoesNotExist:
            self.message = "존재하지 않는 목표입니다."
            isCheck = False

        return isCheck