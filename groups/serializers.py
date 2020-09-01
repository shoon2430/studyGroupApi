from rest_framework.serializers import ModelSerializer
from .models import Group


class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "imageUrl",
            "category",
            "title",
            "discription",
            "leader",
            "time",
        )
