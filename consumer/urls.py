from django.urls import path
from consumer.views import *

urlpatterns = [
    path('consumer-info', ConsumerUserInfo.as_view(), name='consumer_info'),
    path('cafes', CafeList.as_view(), name='cafe_list'),
    path('add-to-favourites/<int:pk>', AddToFavourites.as_view()),
    path('remove-from-favourites/<int:pk>', RemoveFromFavourites.as_view()),
    path('cafes/<int:pk>/ratings', RateCafe.as_view()),
]
