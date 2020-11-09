from rest_framework import generics
from rest_framework.response import Response

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


class Orders(generics.ListCreateAPIView):
    queryset = Order.objects.none()  # Required for DjangoModelPermissions

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        user = self.request.user
        if status:
            if status != 'done' and status != 'active':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Order.objects.filter(consumer=user.consumer).filter(status=status)
        else:
            return Order.objects.filter(consumer=user.consumer)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateOrderSerializer
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.serializer_class = ViewOrderSerializer
        return self.list(request, *args, **kwargs)
