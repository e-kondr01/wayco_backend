from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import *
from common.serializers import CafeSerializer, OrderSerializer
from common.models import Consumer, Order, Cafe


class ConsumerInfo(generics.RetrieveUpdateAPIView):
    serializer_class = ConsumerInfoSerializer
    queryset = User.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class ActiveOrders(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(consumer=user.consumer).filter(status='active')


class OrderHistory(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(consumer=user.consumer).filter(status='done')


class CafeList(generics.ListAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
