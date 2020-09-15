from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

from rest_framework import serializers

from todos.serializers import todoAllSerializer
from .models import User
from groups.models import Group
from todos.models import Subject, TodoGroup, Todo


# class myGroupInnerTodoSerializer(serializers.ModelSerializer):
#     todoList = serializers.SerializerMethodField("todos_set")
#     group_id = serializers.CharField(source="id")

#     class Meta:
#         model = Group
#         fields = (
#             "group_id",
#             "category",
#             "title",
#             "time",
#             "todoList",
#         )

#     def todos_set(self, group):
#         from pprint import pprint

#         pprint(vars(self))

#         # 첫번째 그룹
#         print(group)
#         print("첫번째 그룹")

#         subjects = Subject.objects.filter(group_id=group)
#         todoGroups = TodoGroup.objects.filter(subject_id__in=subjects)
#         todos = Todo.objects.filter(todoGroup_id__in=todoGroups)
#         # 해당 그룹안의 전체 todo
#         pprint(todos)
#         # 내것만 추리자
#         # queryset = todos.filter(writer=user)

#         print("============================")
#         queryset = Todo.objects.all()
#         serializer = todoAllSerializer(instance=queryset, many=True)
#         return serializer.data