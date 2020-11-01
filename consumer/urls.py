from django.urls import path
from .views import *

urlpatterns = [
    path('consumer_info/<int:pk>', ConsumerInfo.as_view(), name='consumer_info'),
    path('active_orders/', ActiveOrders.as_view(), name='active_orders'),
    path('cafes/', CafeList.as_view(), name='cafe_list'),
]
