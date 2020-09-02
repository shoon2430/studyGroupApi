import uuid
from django.urls import path
from .views import createAndShowGroupInfo, attendApplyToGroup, confirmMemberToGroup

app_name = "groups"

urlpatterns = [
    path("groups/", createAndShowGroupInfo.as_view(), name="list"),
    path("groups/<uuid:pk>/attend/", attendApplyToGroup.as_view(), name="attend"),
    path("groups/<uuid:pk>/confirm/", confirmMemberToGroup.as_view(), name="confirm"),
]