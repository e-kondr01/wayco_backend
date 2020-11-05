from rest_framework import generics

from common.models import *
from common.serializers import *


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializerForMenu
    queryset = Product.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        pk = self.kwargs['cafe_pk']
        cafe = Cafe.objects.get(pk=pk)
        return Product.objects.filter(cafe=cafe)


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_pk'


class CreateOrder(generics.CreateAPIView):
    queryset = Order.objects.none()  # Required for DjangoModelPermissions
    serializer_class = CreateOrderSerializer

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)
