from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import *
from common.models import Consumer


class CreateConsumerUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = ConsumerUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateEmployeeUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = EmployeeUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsLoginUnique(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        username = request.data['login']
        if User.objects.filter(username=username):
            resp = {'username_status': 'taken'}
        else:
            resp = {'username_status': 'free'}
        return Response(resp, status=status.HTTP_200_OK)
