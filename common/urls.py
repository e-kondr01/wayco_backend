from django.urls import path
from common.views import *


urlpatterns = [
     path('cafes/<int:cafe_pk>/menu', ProductList.as_view(),
          name='cafe_product_list'),
     path('cafes/<int:cafe_pk>/menu/<int:product_pk>/',
          ProductDetail.as_view(), name='cafe_product_detail'),
     path('orders/', CreateOrder.as_view()),
]
