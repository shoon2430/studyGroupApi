import uuid
from django.urls import path
from .views import (
    subjectCreateApi,
    subjectDetailApi,
    todoCreateApi,
    todoDetailApi,
    subjectInnerTodosListApi,
)

app_name = "todos"

"""
1. subject CRUD

1. todo CRUD

"""


urlpatterns = [
    path(
        "groups/<uuid:group_pk>/test/", subjectInnerTodosListApi.as_view(), name="test"
    ),
    path(
        "groups/<uuid:group_pk>/subjects/", subjectCreateApi.as_view(), name="subjects"
    ),
    path(
        "groups/<uuid:group_pk>/subjects/<uuid:subject_pk>/",
        subjectDetailApi.as_view(),
        name="subject-detail",
    ),
    path(
        "subjects/<uuid:subject_pk>/todos/",
        todoCreateApi.as_view(),
        name="todos",
    ),
    path(
        "subjects/<uuid:subject_pk>/todos/<uuid:todo_pk>/",
        todoDetailApi.as_view(),
        name="todo-detail",
    ),
]
