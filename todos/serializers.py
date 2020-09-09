from rest_framework import serializers
from groups.models import Group
from users.models import User
from users.serializers import UserBaseSerializer
from .models import Subject, Todo

from users.serializers import userSimpleInfoSerializer


class TodoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ("subject_id", "time", "title", "writer", "progress")


class SubjectSimpleSerializer(serializers.ModelSerializer):
    todos = TodoSimpleSerializer(many=True)

    class Meta:
        model = Subject
        fields = ("group_id", "time", "title", "writer", "todos")


class groupSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("group_id", "time", "title", "writer", "todos")


class SubjectBaseSerializer(serializers.ModelSerializer):

    group_id = serializers.UUIDField(read_only=True)
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


class SubjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("title",)