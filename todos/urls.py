import uuid
from django.urls import path
from .views import (
    subjectCreateApi,
    subjectDetailApi,
    todoGroupCreateApi,
    todoGroupDetailApi,
    addUserFromTodoGroupApi,
    todoDetailApi,
)

app_name = "todos"

urlpatterns = [
    path(
        "groups/<uuid:group_pk>/subjects/", subjectCreateApi.as_view(), name="subjects"
    ),
    path(
        "groups/<uuid:group_pk>/subjects/<uuid:subject_pk>/",
        subjectDetailApi.as_view(),
        name="subject-detail",
    ),
    path(
        "subjects/<uuid:subject_pk>/todoGroups/",
        todoGroupCreateApi.as_view(),
        name="todoGroups",
    ),
    path(
        "subjects/<uuid:subject_pk>/todoGroups/<uuid:todoGoup_pk>/",
        todoGroupDetailApi.as_view(),
        name="todoGroup-detail",
    ),
    path(
        "subjects/<uuid:subject_pk>/todoGroups/<uuid:todoGoup_pk>/addUser/",
        addUserFromTodoGroupApi.as_view(),
        name="todoGroup-addUser",
    ),
    path(
        "todoGroups/<uuid:todoGoup_pk>/todos/<uuid:todo_pk>/",
        todoDetailApi.as_view(),
        name="todo-detail",
    ),
]
