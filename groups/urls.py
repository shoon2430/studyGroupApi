from django.urls import path
from .views import createAndShowGroupInfo, attendToGroup

app_name = "groups"

urlpatterns = [
    path("groups/", createAndShowGroupInfo.as_view(), name="all-list"),
    path("groups/<int:pk>/", attendToGroup.as_view(), name="update"),
]