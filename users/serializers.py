from django.contrib.auth.models import update_last_login

from django.contrib.auth import authenticate

from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .models import User

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
        )
        extra_kwargs = {
            # "password": {"write_only": True},
        }


# 회원가입 Serializer
class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField()
    introduce = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            nickname=validated_data["nickname"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])

        user.save()
        return user


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    phone = serializers.CharField()
    introduce = serializers.CharField()

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.introduce = validated_data.get("introduce", instance.introduce)

        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
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
        return {"username": user.username, "token": jwt_token}
