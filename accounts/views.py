from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import *


class CreateConsumerUser(APIView):
    authentication_classes = []
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
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = EmployeeUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                resp = {
                    'registration_result': 'success'
                }
                return Response(data=resp,
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsLoginUnique(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        username = request.data['login']
        if User.objects.filter(username=username):
            resp = {'username_status': 'taken'}
        else:
            resp = {'username_status': 'free'}
        return Response(resp, status=status.HTTP_200_OK)


class CheckGroupView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        resp = {}
        resp['groups'] = []
        for group in request.user.groups.all():
            resp['groups'].append(group.name)
        return Response(resp, status=status.HTTP_200_OK)
