import uuid
from django.urls import path
from .views import subjectCreateApi, subjectDetailApi

app_name = "todos"

"""
1. subject CRUD

1. todo CRUD

"""


urlpatterns = [
    path(
        "group/<uuid:group_pk>/subjects/", subjectCreateApi.as_view(), name="subjects"
    ),
    path(
        "group/<uuid:group_pk>/subject/<uuid:subject_pk>/",
        subjectDetailApi.as_view(),
        name="subject-detail",
    ),
    path(
        "subject/<uuid:subject_pk>/todos/",
        subjectDetailApi.as_view(),
        name="todos",
    ),
    path(
        "subject/<uuid:subject_pk>/todo/<uuid:todo_pk>/",
        subjectDetailApi.as_view(),
        name="todo-detail",
    ),
]
