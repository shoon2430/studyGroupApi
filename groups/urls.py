import uuid
from django.urls import path
from .views import (
    createAndShowGroupInfoApi,
    attendApplyToGroupApi,
    outApplyToGroupApi,
    confirmMemberToGroupApi,
    groupDetailApi,
)

app_name = "groups"

urlpatterns = [
    path("groups/", createAndShowGroupInfoApi.as_view(), name="groups"),
    path("groups/<uuid:pk>/", groupDetailApi.as_view(), name="info"),
    path("groups/<uuid:pk>/attend/", attendApplyToGroupApi.as_view(), name="attend"),
    path("groups/<uuid:pk>/out/", outApplyToGroupApi.as_view(), name="out"),
    path(
        "groups/<uuid:pk>/confirm/", confirmMemberToGroupApi.as_view(), name="confirm"
    ),
]