"""URL configuration for Amenazas endpoint"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AmenazaViewSet

router = DefaultRouter()
router.register(r'', AmenazaViewSet, basename='amenaza')

urlpatterns = [
    path('', include(router.urls)),
]
