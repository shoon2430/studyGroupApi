from rest_framework.serializers import ModelSerializer
from .models import User


class UserBaseSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "name", "phone", "email")
        extra_kwargs = {
            # "username": {"write_only": True},
            "password": {"write_only": True},
            "phone": {"write_only": True},
        }

    def validate(self, data):
        print("test")
        return data
