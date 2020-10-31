from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('new_consumer/', views.CreateConsumerUser.as_view(),
         name='create_consumer_account'),
    path('new_barista/', views.CreateCafeBaristaUser.as_view(),
         name='create_cafe_barista_account'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
