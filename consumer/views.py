from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import *
from common.serializers import (
    CafeSerializer, ViewOrderSerializer, CreateOrderSerializer)
from common.models import Consumer, Order, Cafe


class ConsumerInfo(generics.RetrieveUpdateAPIView):
    serializer_class = ConsumerInfoSerializer
    queryset = User.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class ActiveOrders(generics.ListAPIView):
    serializer_class = ViewOrderSerializer
    queryset = Order.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(consumer=user.consumer).filter(status='active')


class OrderHistory(generics.ListAPIView):
    serializer_class = ViewOrderSerializer
    queryset = Order.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(consumer=user.consumer).filter(status='done')


class CafeList(generics.ListAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer


class CreateOrder(generics.CreateAPIView):
    queryset = Order.objects.none()  # Required for DjangoModelPermissions
    serializer_class = CreateOrderSerializer

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)
