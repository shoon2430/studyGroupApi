from rest_framework import serializers
from .models import Group
from users.models import User
from users.serializers import UserBaseSerializer


class GroupBaseSerializer(serializers.ModelSerializer):
    leader = UserBaseSerializer(read_only=True)
    members = UserBaseSerializer(many=True, read_only=True)
    leader_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Group
        fields = (
            "category",
            "title",
            "discription",
            "leader",
            "leader_id",
            "members",
            "time",
        )

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["leader_id"])
        group = Group.objects.create(
            category=validated_data["category"],
            title=validated_data["title"],
            discription=validated_data["discription"],
            time=validated_data["time"],
            leader=user,
        )
        return group


# 그룹 참여 Serializer
class attendToGroupSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(required=False)

    def __init__(self, group, *args, **kwargs):
        super(attendToGroupSerializer, self).__init__(*args, **kwargs)
        self.group = group

    class Meta:
        model = Group
        fields = ("userId",)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):

        self.group.members.add(User.objects.get(username=validated_data["userId"]))
        return self.group