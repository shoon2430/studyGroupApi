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
            "discription",
            "leader",
            "time",
            "members",
            "attends",
            "subjectList",
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

    def validate(self, data):
        """
        member에 이미 존재하는지 확인
        """
        username = data.get("userId", None)
        try:
            user = User.objects.get(username=username)
            if user not in self.group.attends.all():
                raise serializers.ValidationError("참여목록에 존재하지 않습니다.")
            elif user in self.group.members.all():
                raise serializers.ValidationError("이미 그룹에 참여중인 유저입니다.")

            return data
        except User.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 유저입니다.")

    def create(self, validated_data):
        user = User.objects.get(username=validated_data["userId"])

        self.group.attends.remove(user)
        self.group.members.add(user)

        # 유저 정보에 그룹 정보 추가
        user.attendGroups.add(self.group)
        self.group.save()
        user.save()

        return self.group
