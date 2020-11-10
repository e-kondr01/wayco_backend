from django.utils import timezone
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


class Orders(generics.ListCreateAPIView):
    queryset = Order.objects.none()  # Required for DjangoModelPermissions

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        user = self.request.user
        if status:
            if status != 'completed' and status != 'active':
                return Order.objects.none()
            else:
                if user.groups.filter(name='consumers'):
                    return Order.objects.filter(consumer=user.consumer).filter(status=status)
                elif user.groups.filter(name='employees'):
                    cafe = user.employee.cafe
                    return Order.objects.filter(cafe=cafe).filter(status=status)
                else:
                    return Order.objects.none()
        else:
            return Order.objects.none()

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateOrderSerializer
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        status = request.query_params.get('status', None)
        if request.user.groups.filter(name='consumers'):
            if status == 'active':
                self.serializer_class = ViewActiveOrderSerializerForConsumer
            elif status == 'completed':
                self.serializer_class = ViewCompletedOrderSerializerForConsumer
        elif request.user.groups.filter(name='employees'):
            if status == 'active':
                self.serializer_class = ViewActiveOrderSerializerForEmployee
            elif status == 'completed':
                self.serializer_class = ViewCompletedOrderSerializerForEmployee

        return self.list(request, *args, **kwargs)


class UpdateOrder(generics.UpdateAPIView):
    serializer_class = ViewCompletedOrderSerializerForEmployee
    queryset = Order.objects.all()  # Required for DjangoModelPermissions

    def filter_queryset(self, queryset):
        return queryset.filter(cafe=self.request.user.employee.cafe)

    def perform_update(self, serializer):
        if serializer.validated_data['status'] == 'ready':
            serializer.save(ready_at=timezone.now())
        elif serializer.validated_data['status'] == 'completed':
            serializer.save(completed_at=timezone.now())
