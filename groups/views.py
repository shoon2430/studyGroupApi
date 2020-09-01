from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GroupBaseSerializer, attendToGroupSerializer
from .models import Group


class createAndShowGroupInfo(APIView):
    def get(self, request):
        print(Group.objects.all())
        serializer = GroupBaseSerializer(Group.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = GroupBaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)


class attendToGroup(APIView):
    def get_object(self, pk):
        return Group.objects.get(pk=pk)

    def put(self, request, pk):
        testmodel_object = self.get_object(pk)
        serializer = attendToGroupSerializer(group=testmodel_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
