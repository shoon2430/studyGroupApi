import uuid
from django.urls import path
from .views import (
    createAndShowGroupInfo,
    attendApplyToGroup,
    confirmMemberToGroup,
    groupDetailApi,
)

app_name = "groups"

urlpatterns = [
    path("groups/", createAndShowGroupInfo.as_view(), name="groups"),
    path("groups/<uuid:pk>/", groupDetailApi.as_view(), name="info"),
    path("groups/<uuid:pk>/attend/", attendApplyToGroup.as_view(), name="attend"),
    path("groups/<uuid:pk>/confirm/", confirmMemberToGroup.as_view(), name="confirm"),
]