from django.urls import path
from .views import createUserView

app_name = "users"

urlpatterns = [path("users/", createUserView.as_view(), name="create")]
