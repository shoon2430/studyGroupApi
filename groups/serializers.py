from rest_framework import serializers
from .models import Group
from users.models import User
from users.serializers import UserBaseSerializer


# class GroupPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#     photo = serializers.ImageField(use_url=True)


class GroupBaseSerializer(serializers.ModelSerializer):
    leader = UserBaseSerializer(read_only=True)
    time = serializers.IntegerField(read_only=True)
    members = UserBaseSerializer(many=True, read_only=True)
    attends = UserBaseSerializer(many=True, read_only=True)

    def __init__(self, leader, *args, **kwargs):
        super(GroupBaseSerializer, self).__init__(*args, **kwargs)
        self.leader = leader

    class Meta:
        model = Group
        fields = (
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


# # 그룹 참여 Serializer
# class attendToGroupSerializer(serializers.ModelSerializer):
#     userId = serializers.CharField(required=False)

#     def __init__(self, group, user, *args, **kwargs):
#         super(attendToGroupSerializer, self).__init__(*args, **kwargs)
#         self.group = group

#     class Meta:
#         model = Group
#         fields = ("userId",)

#     def create(self, validated_data):
#         self.group.attends.add(user)
#         return self.group


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