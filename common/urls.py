from django.urls import path

from .views import *


urlpatterns = [
     path('cafes/<int:cafe_pk>/menu', Products.as_view()),
     path('cafes/<int:cafe_pk>/menu/<int:product_pk>',
          ProductDetail.as_view()),
     path('orders', Orders.as_view()),
     path('orders/<int:pk>', UpdateOrder.as_view()),
     path('cafes', Cafes.as_view()),
     path('cafes/<int:pk>', CafeDetail.as_view()),
]
