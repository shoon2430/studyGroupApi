from django.urls import path
from .views import (
    showUserApi,
    userLoginAPI,
    createUserApi,
    userDetailApi,
    deleteUserApi,
)
from .user_management_views import userInnerGroupsApi, userInnerTodosApi

from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

app_name = "users"

urlpatterns = [
    # 일단 임시로 보류
    path("jwt-auth/", obtain_jwt_token, name="get-token"),  # JWT 토큰 획득
    path("jwt-auth/refresh/", refresh_jwt_token),  # JWT 토큰 갱신
    path("jwt-auth/verify/", verify_jwt_token),  # JWT 토큰 확인
    # 유저관련 URL
    path("users/", showUserApi.as_view(), name="list"),
    path("signin/", createUserApi.as_view(), name="create"),
    path("login/", userLoginAPI.as_view(), name="login"),
    path("out-member/", deleteUserApi.as_view(), name="delete"),
    path("modify-info/", userDetailApi.as_view(), name="modify"),
    # 나의 정보 관련 URL
    # 내가속한 그룹조회
    path("user/groups", userInnerGroupsApi.as_view(), name="user-groups"),
    # 내가 해야할 todoList조회
    path("user/todos", userInnerTodosApi.as_view(), name="user-todos"),
]
