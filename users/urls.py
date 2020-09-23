from django.urls import path
from .views import (
    showUserApi,
    userLoginAPI,
    createUserApi,
    userDetailApi,
    deleteUserApi,
    validateUserIdApi,
    userChangePasswordApi,
)

from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from .user_managemet_urls import user_management_urlpatterns

app_name = "users"

users_urlpatterns = [
    # 일단 임시로 보류
    path("jwt-auth/", obtain_jwt_token, name="get-token"),  # JWT 토큰 획득
    path("jwt-auth/refresh/", refresh_jwt_token),  # JWT 토큰 갱신
    path("login/verify/", verify_jwt_token),  # JWT 토큰 확인
    # 유저관련 URL
    path("users/", showUserApi.as_view(), name="list"),
    path("signin/", createUserApi.as_view(), name="create"),
    path("login/", userLoginAPI.as_view(), name="login"),
    path("users/validate/", validateUserIdApi.as_view(), name="userId"),
    path("out-member/", deleteUserApi.as_view(), name="delete"),
    path("users/info/", userDetailApi.as_view(), name="modify"),
    path("users/password/", userChangePasswordApi.as_view(), name="password"),
]

urlpatterns = users_urlpatterns + user_management_urlpatterns
