from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status as drf_status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *


class Products(generics.ListCreateAPIView):
    '''Cafe menu'''
    serializer_class = ProductSerializerForMenu

    def get_queryset(self):
        pk = self.kwargs['cafe_pk']
        cafe = Cafe.objects.get(pk=pk)
        return Product.objects.filter(cafe=cafe).filter(on_menu=True)

    def create(self, request, *args, **kwargs):
        '''The first line is changed to have different
         serializers for retrieve and create'''
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=drf_status.HTTP_201_CREATED,
            headers=headers)

    def perform_create(self, serializer):
        serializer.save(cafe=self.request.user.employee.cafe)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    '''This view handles all CRUD operations for cafe's products'''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_pk'

    def get_queryset(self):
        if self.request.method == 'GET':
            return Product.objects.all()
        else:
            cafe = self.request.user.employee.cafe
            return Product.objects.filter(cafe=cafe)

    def update(self, request, *args, **kwargs):
        '''We want to handle both PUT/PATCH updates and
        creation of a new product instead of actually updating.
        Patch requests shold be able to change only the availability '''
        if request.method == 'PATCH':
            resp = self.change_availability(request, *args, **kwargs)
            return resp
        elif request.method == 'PUT':
            resp = self.create_new_version(request, *args, **kwargs)
            return resp

    def change_availability(self, request, *args, **kwargs):
        '''We want to let employees change only the availability,
        but return all info about the product '''
        availability = request.data.get('available', 'no info')
        if availability != 'no info':
            data = {'available': request.data['available']}
        else:
            return Response(status=drf_status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create_new_version(self, request, *args, **kwargs):
        instance = self.get_object()

        '''We want to actually create a new object '''
        serializer = ProductSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        '''Keeping the previous version, but removing it from the menu '''
        instance.on_menu = False
        instance.save()

        serializer.save(on_menu=True, cafe=self.request.user.employee.cafe)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=drf_status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        '''Do not delete the object from database, but
        remove it from the menu '''
        instance = self.get_object()
        if not instance.on_menu:
            data = {
                'error': 'This product has already been removed from menu'
            }
            return Response(data=data, status=drf_status.HTTP_400_BAD_REQUEST)
        else:
            instance.on_menu = False
            instance.save()
            data = {
                'success': ('This product has been successfuly removed '
                            'from menu')
            }
            return Response(data=data, status=drf_status.HTTP_204_NO_CONTENT)


class Orders(generics.ListCreateAPIView):

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
                    if status == 'completed':
                        statuses = ['claimed', 'ready', 'unclaimed']
                        return Order.objects.filter(
                            consumer=user.consumer).filter(status__in=statuses)
                    else:
                        return Order.objects.filter(
                            consumer=user.consumer).filter(status=status)
                elif user.groups.filter(name='employees'):
                    cafe = user.employee.cafe
                    '''We want to return only
                    orders that are the same day
                    for employee '''
                    if status == 'completed':
                        statuses = ['claimed', 'ready', 'unclaimed']
                        return Order.objects.filter(
                            cafe=cafe).filter(
                            status__in=statuses).filter(
                            created_at__gte=timezone.now()-timedelta(days=1))
                    else:
                        return Order.objects.filter(
                            cafe=cafe).filter(
                            status=status).filter(
                            created_at__gte=timezone.now()-timedelta(days=1))
                elif user.groups.filter(name='cafe_admin'):
                    cafe = user.employee.cafe
                    return Order.objects.filter(
                        cafe=cafe).filter(status=status)
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
        elif (serializer.validated_data['status'] == 'claimed'
              or serializer.validated_data['status'] == 'unclaimed'):
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
            rating_object = request.user.consumer.ratings.filter(
                cafe=cafe).first()
            if rating_object:
                rating = rating_object.value
            else:
                rating = None
            cafe_info['user_rating'] = rating

        return Response(resp)


class CafeDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CafeSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Cafe.objects.none()
        if self.request.method == 'GET':
            return Cafe.objects.all()
        elif self.request.method == 'PUT':
            cafe = self.request.user.employee.cafe
            return Cafe.objects.filter(pk=cafe.pk)
        else:
            return Cafe.objects.none()


class ConsumerUserInfo(generics.RetrieveAPIView):
    ''' Get consumer info'''
    serializer_class = ConsumerUserInfoSerializer
    queryset = Consumer.objects.none()  # Required for DjangoModelPermissions

    def get_object(self):
        obj = get_object_or_404(User, pk=self.request.user.pk)
        return obj


class AddToFavourites(APIView):
    queryset = Consumer.objects.none()  # Required for DjangoModelPermissions

    def get(self, request, pk):
        consumer = get_object_or_404(Consumer, pk=request.user.consumer.pk)
        cafe = get_object_or_404(Cafe, pk=pk)
        consumer.favourite_cafes.add(cafe)
        return Response(status=drf_status.HTTP_200_OK)


class RemoveFromFavourites(APIView):
    queryset = Consumer.objects.none()  # Required for DjangoModelPermissions

    def get(self, request, pk):
        consumer = get_object_or_404(Consumer, pk=request.user.consumer.pk)
        cafe = get_object_or_404(Cafe, pk=pk)
        consumer.favourite_cafes.remove(cafe)
        return Response(status=drf_status.HTTP_200_OK)


class RateCafe(generics.CreateAPIView):
    queryset = CafeRating.objects.all()
    serializer_class = CafeRatingSerializer

    def create(self, request, *args, **kwargs):
        cafe = get_object_or_404(Cafe, pk=self.kwargs['pk'])

        '''If user has already rated this cafe,
        we have to delete the previous rating '''
        old_rating = CafeRating.objects.filter(
            consumer=request.user.consumer).filter(cafe=cafe)

        if old_rating:
            old_rating.delete()

        data = request.data
        data['cafe'] = cafe.pk
        data['consumer'] = request.user.consumer.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        ''' Update cafe's average rating '''
        avg_rating = 0
        cafe_ratings = CafeRating.objects.filter(cafe=cafe)

        for rating in cafe_ratings:
            avg_rating += rating.value
        avg_rating /= len(cafe_ratings)
        cafe.average_rating = round(avg_rating, 1)

        cafe.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=drf_status.HTTP_201_CREATED,
                        headers=headers)
