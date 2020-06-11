from django.urls import path
from .views import UserCreateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializers import CustomTokenPairSerializer

urlpatterns = [
    path(
        'register/',
        UserCreateView.as_view(),
        name="register"
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(
            serializer_class=CustomTokenPairSerializer,
        ),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
