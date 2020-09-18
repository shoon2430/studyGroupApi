from rest_framework import serializers
from .models import Group
from users.models import User
from users.serializers import UserBaseSerializer, userSimpleInfoSerializer

from todos.serializers import SubjectSimpleSerializer


class GroupBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    leader = userSimpleInfoSerializer(read_only=True)
    time = serializers.IntegerField(read_only=True)
    members = userSimpleInfoSerializer(many=True, read_only=True)
    attends = userSimpleInfoSerializer(many=True, read_only=True)

    def __init__(self, leader, *args, **kwargs):
        super(GroupBaseSerializer, self).__init__(*args, **kwargs)
        self.leader = leader

    class Meta:
        model = Group
        fields = (
            "id",
            "category",
            "title",
            "description",
            "leader",
            "time",
            "members",
            "attends",
        )

    def create(self, validated_data):
        group = Group.objects.create(
            category=validated_data["category"],
            title=validated_data["title"],
            description=validated_data["description"],
            leader=self.leader,
        )
        group.members.add(self.leader)
        group.save()
        self.leader.attendGroups.add(group)
        self.leader.save()
        return group


# 그룹 상세 정보 조회
class GroupInfoShowSerializer(serializers.ModelSerializer):
    subjectList = SubjectSimpleSerializer(source="group", many=True)
    members = userSimpleInfoSerializer(many=True)
    attends = userSimpleInfoSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "category",
            "title",
            "description",
            "leader",
            "time",
            "members",
            "attends",
            "subjectList",
        )


# 그룹 상세 정보 수정
class GroupInfoUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Group
        fields = (
            "category",
            "title",
            "description",
        )
