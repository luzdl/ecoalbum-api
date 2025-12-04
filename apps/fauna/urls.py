"""Fauna URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, AnimalViewSet, AmenazaViewSet, AccionProteccionViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'fauna', AnimalViewSet, basename='fauna')
router.register(r'amenazas', AmenazaViewSet, basename='amenaza')
router.register(r'acciones-proteccion', AccionProteccionViewSet, basename='accion-proteccion')

urlpatterns = router.urls
