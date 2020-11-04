from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from common.serializers import (
    CafeSerializer, ViewOrderSerializer, CreateOrderSerializer)
from common.models import Consumer, Order, Cafe


class ConsumerUserInfo(generics.RetrieveAPIView):
    ''' Get consumer info'''
    serializer_class = ConsumerUserInfoSerializer
    queryset = Consumer.objects.none()  # Required for DjangoModelPermissions

    def get_object(self):
        obj = get_object_or_404(User, pk=self.request.user.pk)
        return obj


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


class AddToFavourites(APIView):
    queryset = Consumer.objects.none()  # Required for DjangoModelPermissions

    def get(self, request, pk):
        consumer = get_object_or_404(Consumer, pk=request.user.consumer.pk)
        cafe = get_object_or_404(Cafe, pk=pk)
        consumer.favourite_cafes.add(cafe)
        return Response(status=status.HTTP_200_OK)


class RemoveFromFavourites(APIView):
    queryset = Consumer.objects.none()  # Required for DjangoModelPermissions

    def get(self, request, pk):
        consumer = get_object_or_404(Consumer, pk=request.user.consumer.pk)
        cafe = get_object_or_404(Cafe, pk=pk)
        consumer.favourite_cafes.remove(cafe)
        return Response(status=status.HTTP_200_OK)


class RateCafe(generics.CreateAPIView):
    queryset = CafeRating.objects.all()
    serializer_class = CafeRatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cafe = Cafe.objects.get(pk=request.data['cafe'])
        old_rating = CafeRating.objects.filter(consumer=request.user.consumer).filter(cafe=cafe)

        if old_rating:
            old_rating.delete()

        serializer.save(consumer=request.user.consumer)

        ''' Update cafe's average rating '''
        avg_rating = 0
        cafe_ratings = CafeRating.objects.filter(cafe=cafe)
        for rating in cafe_ratings:
            avg_rating += rating.value
        avg_rating /= len(cafe_ratings)
        cafe.average_rating = round(avg_rating, 1)
        cafe.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
