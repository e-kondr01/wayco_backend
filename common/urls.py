from django.urls import path
from common.views import *

urlpatterns = [
    path('cafes/', CafeList.as_view(), name='cafe_list'),
    path('cafes/<int:pk>/menu', ProductList.as_view(), name='cafe_product_list'),
]
