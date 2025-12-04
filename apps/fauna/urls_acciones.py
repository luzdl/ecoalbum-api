"""URL configuration for Acciones de Proteccion endpoint"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccionProteccionViewSet

router = DefaultRouter()
router.register(r'', AccionProteccionViewSet, basename='accion-proteccion')

urlpatterns = [
    path('', include(router.urls)),
]
