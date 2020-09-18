from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .models import User


class userSimpleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
        )


# 기본 유저정보 조회 Serializer
class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "nickname",
            "phone",
            "email",
            "introduce",
            "attendGroups",
            "date_joined",
        )
        extra_kwargs = {
            # "password": {"write_only": True},
        }


# 회원가입 Serializer
class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    phone = serializers.CharField(allow_blank=True)
    introduce = serializers.CharField(allow_blank=True)

    def create(self, validated_data):

        if User.objects.filter(username=validated_data["username"]).first() is None:
            user = User.objects.create(
                username=validated_data["username"],
                nickname=validated_data["nickname"],
                email=validated_data["email"],
                phone=validated_data.get("phone", None),
                introduce=validated_data.get("introduce", None),
            )
            user.set_password(validated_data["password"])

            user.save()
            return user
        else:
            raise serializers.ValidationError("이미 존재하는 아이디 입니다.")


class UserUpdateSerializer(serializers.Serializer):
    nickname = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    introduce = serializers.CharField(allow_blank=True)

    def validate(self, data):
        phone = data.get("phone", None)
        return data

    def update(self, instance, validated_data):

        instance.email = (
            instance.email if validated_data["email"] == "" else validated_data["email"]
        )
        instance.nickname = (
            instance.nickname
            if validated_data["nickname"] == ""
            else validated_data["nickname"]
        )
        instance.phone = (
            instance.phone if validated_data["phone"] == "" else validated_data["phone"]
        )
        instance.introduce = (
            instance.introduce
            if validated_data["introduce"] == ""
            else validated_data["introduce"]
        )

        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    nickname = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        try:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("아이디와 비밀번호를 확인해주세요")

            payload = jwt_payload_handler(user)
            jwt_token = jwt_encode_handler(payload)

        except User.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 유저입니다.")
        return {
            "username": user.username,
            "nickname": user.nickname,
            "token": jwt_token,
        }
