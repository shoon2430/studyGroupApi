from django.urls import path
from .user_management_views import (
    userInnerGroupsApi,
    userInnerTodosApi,
    leaderInnerGroupsApi,
)

# 나의 정보 관련 URL
# 내가속한 그룹조회
user_management_urlpatterns = [
    path("user/groups", userInnerGroupsApi.as_view(), name="user-groups"),
    # 내가 해야할 todoList조회
    path("leader/groups", leaderInnerGroupsApi.as_view(), name="leader-gorup"),
    path("user/todos", userInnerTodosApi.as_view(), name="user-todos"),
]