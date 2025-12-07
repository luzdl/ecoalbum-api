"""Flora URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FloraViewSet

router = DefaultRouter()
router.register(r'flora', FloraViewSet, basename='flora')

urlpatterns = router.urls
