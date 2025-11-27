"""
URL configuration for ecoalbum_api project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.core.views import HealthCheckView
from apps.species.views import CategoryViewSet, SpeciesViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'species', SpeciesViewSet, basename='species')

schema_view = get_schema_view(
    openapi.Info(
        title='Ecoalbum API',
        default_version='v1',
        description='API for cataloging protected fauna and flora species in Panama',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='info@ecoalbum.com'),
        license=openapi.License(name='MIT'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/', include(router.urls)),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/schema/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/openapi.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
