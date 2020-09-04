from django.urls import path
from .views import (
    showUserApi,
    userLoginAPI,
    createUserApi,
    updateUserApi,
    deleteUserApi,
)
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

app_name = "users"

urlpatterns = [
    path("jwt-auth/", obtain_jwt_token, name="get-token"),  # JWT 토큰 획득
    path("jwt-auth/refresh/", refresh_jwt_token),  # JWT 토큰 갱신
    path("jwt-auth/verify/", verify_jwt_token),  # JWT 토큰 확인
    path("users/", showUserApi.as_view(), name="list"),
    path("signin/", createUserApi.as_view(), name="create"),
    path("login/", userLoginAPI.as_view(), name="login"),
    path("out-member/", deleteUserApi.as_view(), name="delete"),
    path("user/<username>/modify/", updateUserApi.as_view(), name="modify"),
    path("user/<username>/delete/", deleteUserApi.as_view(), name="delete"),
]
