from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status as drf_status
from rest_framework.response import Response

from .models import *
from .serializers import *


class Products(generics.ListCreateAPIView):
    serializer_class = ProductSerializerForMenu
    queryset = Product.objects.none()  # Required for DjangoModelPermissions

    def get_queryset(self):
        pk = self.kwargs['cafe_pk']
        cafe = Cafe.objects.get(pk=pk)
        return Product.objects.filter(cafe=cafe)

    def create(self, request, *args, **kwargs):
        '''The first line is changed to have different serializers for retreive and create'''
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=drf_status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(cafe=self.request.user.employee.cafe)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_pk'

    def get_permitted_queryset(self):
        '''This method was changed so that employee can't edit or delete products from other cafes'''
        cafe = self.request.user.employee.cafe
        return Product.objects.filter(cafe=cafe)

    def get_permitted_object(self):
        queryset = self.filter_queryset(self.get_permitted_queryset())  # This line was changed

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_permitted_object()  # This line is changed
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_permitted_object()  # This line was changed
        self.perform_destroy(instance)
        return Response(status=drf_status.HTTP_204_NO_CONTENT)


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


class Cafes(generics.ListAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        resp = serializer.data
        for cafe_info in resp:
            cafe = Cafe.objects.get(pk=cafe_info['id'])
            rating_object = request.user.consumer.ratings.filter(cafe=cafe).first()
            if rating_object:
                rating = rating_object.value
            else:
                rating = None
            cafe_info['user_rating'] = rating

        return Response(resp)


class CafeDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateCafeSerializer

    def get_queryset(self):
        cafe = self.request.user.employee.cafe
        return Cafe.objects.filter(pk=cafe.pk)
