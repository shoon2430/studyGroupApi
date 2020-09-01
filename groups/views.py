from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GroupListSerializer
from .models import Group


class showAllGroupList(APIView):
    def get(self, request):
        serializer = GroupListSerializer(Group.objects.all(), many=True)
        return Response(serializer.data)