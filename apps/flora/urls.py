"""Flora URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FloraViewSet

router = DefaultRouter()
router.register(r'', FloraViewSet, basename='flora')

app_name = 'flora'

urlpatterns = [
    path('', include(router.urls)),
]
