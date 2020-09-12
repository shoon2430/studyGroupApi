from rest_framework import serializers
from groups.models import Group
from users.models import User
from users.serializers import UserBaseSerializer
from .models import Subject, Todo, TodoGroup
from users.models import User

from users.serializers import userSimpleInfoSerializer


class todoAllSerializer(serializers.ModelSerializer):
    todo_id = serializers.CharField(source="id")
    writer = userSimpleInfoSerializer()

    class Meta:
        model = Todo
        fields = ("todo_id", "todoGroup_id", "time", "writer", "progress")


class TodoGroupSimpleSerializer(serializers.ModelSerializer):
    todoGroup_id = serializers.CharField(source="id")
    todoList = todoAllSerializer(source="todo_group", many=True)
    leader = userSimpleInfoSerializer()
    members = userSimpleInfoSerializer(many=True)

    class Meta:
        model = TodoGroup
        fields = (
            "todoGroup_id",
            "subject_id",
            "title",
            "progress",
            "time",
            "leader",
            "members",
            "todoList",
        )


class SubjectSimpleSerializer(serializers.ModelSerializer):
    todoGroups = TodoGroupSimpleSerializer(source="subject", many=True)
    subject_id = serializers.CharField(source="id")
    writer = userSimpleInfoSerializer()

    class Meta:
        model = Subject
        fields = ("subject_id", "time", "title", "writer", "todoGroups")


class groupSubjectsSerializer(serializers.ModelSerializer):
    writer = userSimpleInfoSerializer()

    class Meta:
        model = Subject
        fields = ("id", "time", "title", "writer")


class todosInnerUserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="id")

    class Meta:
        model = User
        fields = (
            "user_id",
            "username",
            "nickname",
        )


class subjectInnerTodoSerializer(serializers.ModelSerializer):
    userList = serializers.SerializerMethodField("users_set")
    todo_id = serializers.CharField(source="id")

    class Meta:
        model = Todo
        fields = ("todo_id", "time", "title", "writer", "progress", "userList")

    def users_set(self, todo):
        queryset = User.objects.filter()
        serializer = todosInnerUserSerializer(instance=queryset, many=True)
        return serializer.data


class SubjectBaseSerializer(serializers.ModelSerializer):

    group_id = serializers.UUIDField(source="group_id", read_only=True)
    time = serializers.IntegerField(read_only=True)
    writer = userSimpleInfoSerializer(read_only=True)

    def __init__(self, group, leader, *args, **kwargs):
        super(SubjectBaseSerializer, self).__init__(*args, **kwargs)
        self.group = group
        self.leader = leader

    class Meta:
        model = Subject
        fields = (
            "group_id",
            "time",
            "title",
            "writer",
        )

    def create(self, validated_data):

        subject = Subject.objects.create(
            title=validated_data["title"],
            time=self.group.time,
            group_id=self.group,
            writer=self.leader,
        )
        return subject


# Subject 수정 및 삭제를 위한 Serializer
class SubjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("title",)


class todoSimpleSerializer(serializers.ModelSerializer):
    subject_id = serializers.UUIDField(read_only=True)
    time = serializers.IntegerField(read_only=True)
    progress = serializers.CharField(read_only=True)
    writer = userSimpleInfoSerializer(read_only=True)

    def __init__(self, subject, writer, *args, **kwargs):
        super(todoSimpleSerializer, self).__init__(*args, **kwargs)
        self.subject = subject
        self.writer = writer

    class Meta:
        model = Todo
        fields = (
            "subject_id",
            "time",
            "title",
            "writer",
            "progress",
        )

    def create(self, validated_data):
        todo = Todo.objects.create(
            title=validated_data["title"],
            time=self.subject.time,
            togoGroup_id=self.subject,
            writer=self.writer,
        )
        return todo


class todoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            "title",
            "progress",
        )
