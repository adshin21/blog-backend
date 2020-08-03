from django.urls import path
from .views import UserCreateView, SocialLoginView

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
        'social/token/',
        SocialLoginView.as_view(),
        name='social-login'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
