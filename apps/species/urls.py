"""Species app URL configuration"""
from django.urls import path
from .views import CategoryViewSet, SpeciesViewSet
from rest_framework.routers import DefaultRouter

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'species', SpeciesViewSet, basename='species')

# urls.py will include these routes
urlpatterns = router.urls
