from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserBaseSerializer
from .models import User


class createUserView(APIView):
    def get(self, request):
        serializer = UserBaseSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserBaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
