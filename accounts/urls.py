from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('consumers', views.CreateConsumerUser.as_view()),
    path('employees', views.CreateEmployeeUser.as_view()),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('login-unique', views.IsLoginUnique.as_view())
]
