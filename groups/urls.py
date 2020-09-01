from django.urls import path
from .views import showAllGroupList

app_name = "groups"

urlpatterns = [path("groups/", showAllGroupList.as_view(), name="all-list")]