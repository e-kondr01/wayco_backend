from rest_framework import generics

from common.models import *
from common.serializers import ProductSerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        pk = self.kwargs['cafe_pk']
        cafe = Cafe.objects.get(pk=pk)
        return Product.objects.filter(cafe=cafe)


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_pk'
