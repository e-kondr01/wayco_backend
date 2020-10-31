from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from common.models import *
from common.serializers import CafeSerializer, ProductSerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions | IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs['cafe_pk']
        cafe = Cafe.objects.get(pk=pk)
        return Product.objects.filter(cafe=cafe)


class CafeList(generics.ListAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = [DjangoModelPermissions]


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_pk'
    permission_classes = [DjangoModelPermissions]
