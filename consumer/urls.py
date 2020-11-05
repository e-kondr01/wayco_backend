from django.urls import path
from .views import *

urlpatterns = [
    path('consumer_info/', ConsumerUserInfo.as_view(), name='consumer_info'),
    path('orders/active/', ActiveOrders.as_view(), name='active_orders'),
    path('orders/history/', OrderHistory.as_view(), name='order_history'),
    path('cafes/', CafeList.as_view(), name='cafe_list'),
    path('add_to_favourites/<int:pk>/', AddToFavourites.as_view()),
    path('remove_from_favourites/<int:pk>/', RemoveFromFavourites.as_view()),
    path('rate_cafe/', RateCafe.as_view()),
]
