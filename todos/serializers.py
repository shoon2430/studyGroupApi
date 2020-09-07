from rest_framework import serializers
from groups.models import Group
from users.models import User
from users.serializers import UserBaseSerializer
from .models import Subject, Todo

from users.serializers import userSimpleInfoSerializer


class SubjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "group_id",
            "time",
            "title",
            "writer",
        )


class SubjectBaseSerializer(serializers.ModelSerializer):

    group_id = serializers.UUIDField(read_only=True)
    time = serializers.IntegerField(read_only=True)
    writer = userSimpleInfoSerializer()

    def __init__(self, group, leader, *args, **kwargs):
        super(SubjectBaseSerializer, self).__init__(*args, **kwargs)
        self.group = group
        self.user = leader

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
        return super().create(validated_data)