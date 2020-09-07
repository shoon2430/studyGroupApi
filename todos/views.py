from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import (
    SubjectBaseSerializer,
)

from .models import Subject, Todo
from core.decode_jwt import request_get_user



class createGroupSubject(APIView):
    '''
    subject 생성
    '''

    permission_classes = []
    authentication_classes = ()

    def post(self, request, pk):

        serializer = SubjectBaseSerializer(
            group=get_object_or_404(Group, pk=pk),
            leader=request_get_user(request),
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
