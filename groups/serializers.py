from rest_framework import serializers
from .models import Group
from users.models import User
from users.serializers import UserBaseSerializer, userSimpleInfoSerializer

from todos.serializers import SubjectSimpleSerializer


class GroupBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    leader = UserBaseSerializer(read_only=True)
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
            "discription",
            "leader",
            "time",
            "members",
            "attends",
        )

    def create(self, validated_data):
        group = Group.objects.create(
            category=validated_data["category"],
            title=validated_data["title"],
            discription=validated_data["discription"],
            leader=self.leader,
        )
        return group


# 그룹 상세 정보 조회
class GroupInfoShowSerializer(serializers.ModelSerializer):
    subjects = SubjectSimpleSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "category",
            "title",
            "discription",
            "leader",
            "time",
            "members",
            "attends",
            "subjects",
        )


# 그룹 상세 정보 수정
class GroupInfoUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    discription = serializers.CharField(allow_blank=True)

    class Meta:
        model = Group
        fields = (
            "category",
            "title",
            "discription",
        )


# 그룹 참가 승인
class confirmToGroupSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(required=False)

    def __init__(self, group, *args, **kwargs):
        super(confirmToGroupSerializer, self).__init__(*args, **kwargs)
        self.group = group

    class Meta:
        model = Group
        fields = ("userId",)

    def create(self, validated_data):

        user = User.objects.get(username=validated_data["userId"])
        self.group.attends.remove(user)
        self.group.members.add(user)
        return self.group