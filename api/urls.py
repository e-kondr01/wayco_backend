from django.urls import path

from .views import *


urlpatterns = [
     path('cafes/<int:cafe_pk>/menu', Products.as_view()),
     path('cafes/<int:cafe_pk>/menu/<int:product_pk>',
          ProductDetail.as_view()),
     path('orders', OrdersView.as_view()),
     path('orders/<int:pk>', UpdateOrder.as_view()),
     path('cafes', Cafes.as_view()),
     path('cafes/<int:pk>', CafeDetail.as_view()),

     path('consumer-info', ConsumerUserInfo.as_view(), name='consumer_info'),
     path('add-to-favourites/<int:pk>', AddToFavourites.as_view()),
     path('remove-from-favourites/<int:pk>', RemoveFromFavourites.as_view()),
     path('cafes/<int:pk>/ratings', RateCafe.as_view()),
]
