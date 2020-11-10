from django.urls import path
from common.views import *


urlpatterns = [
     path('cafes/<int:cafe_pk>/menu', ProductList.as_view(),
          name='cafe_product_list'),
     path('cafes/<int:cafe_pk>/menu/<int:product_pk>', ProductDetail.as_view()),
     path('orders', Orders.as_view()),
     path('orders/<int:pk>', UpdateOrder.as_view()),
]
