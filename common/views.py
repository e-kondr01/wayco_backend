from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from common.models import *
from common.serializers import CafeSerializer, ProductSerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):      
        pk = self.kwargs['pk']
        cafe = Cafe.objects.get(pk=pk)
        return Product.objects.filter(cafe=cafe)


class CafeList(generics.ListAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
