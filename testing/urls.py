from django.urls import path
from .views import Testing

urlpatterns = [
    path('', Testing.as_view(), name="testing"),
]
