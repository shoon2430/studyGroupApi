from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

from rest_framework import serializers

from todos.serializers import todoAllSerializer
from todos.serializers import SubjectSimpleSerializer
from .models import User
from groups.models import Group
from todos.models import Subject, TodoGroup, Todo

# 그룹 상세 정보 조회
class myGroupInfoSerializer(serializers.ModelSerializer):
    subjectList = SubjectSimpleSerializer(source="group", many=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "title",
            "category",
            "description",
            "subjectList",
        )


class myGroupInnerTodoSerializer(serializers.ModelSerializer):
    group_id = serializers.CharField(source="id")

    class Meta:
        model = Group
        fields = (
            "group_id",
            "category",
            "title",
            "time",
        )


class DeviceSerializer(serializers.Serializer):
    group = myGroupInnerTodoSerializer()
    todoList = serializers.SerializerMethodField("todos_set")

    def todos_set(self, obj):
        serializer = todoAllSerializer(instance=obj.todos, many=True)
        return serializer.data