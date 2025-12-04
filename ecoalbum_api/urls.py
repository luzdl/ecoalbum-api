"""
URL configuration for ecoalbum_api project.

API Endpoints:
- /api/fauna/                    - CRUD animales
- /api/fauna/{id}/fotos/         - Fotos de un animal
- /api/fauna/{id}/amenazas/      - Amenazas de un animal
- /api/fauna/{id}/acciones/      - Acciones de protección
- /api/categorias/               - Categorías de fauna
- /api/amenazas/                 - Todas las amenazas
- /api/acciones-proteccion/      - Todas las acciones
- /api/flora/                    - CRUD plantas
- /api/flora/{id}/fotos/         - Fotos de una planta
- /api/galeria/destacados/       - Fotos destacadas (carrusel)
- /api/galeria/aleatorios/       - Fotos aleatorias
- /api/galeria/estadisticas/     - Estadísticas generales
- /api/health/                   - Health check
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.core.views import HealthCheckView

schema_view = get_schema_view(
    openapi.Info(
        title='Ecoalbum API',
        default_version='v1',
        description='''
API para el catálogo de fauna y flora protegida de Panamá.

## Funcionalidades principales:
- **Fauna**: Consulta y filtrado de animales por categoría, estado de conservación, letra inicial
- **Flora**: Consulta y filtrado de plantas
- **Galería**: Endpoints para carrusel y fotos aleatorias
- **Filtros**: Búsqueda, paginación, ordenamiento

## Estados de conservación:
- LC: Preocupación menor
- NT: Casi amenazado  
- VU: Vulnerable
- EN: En peligro
- CR: Peligro crítico
        ''',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='info@ecoalbum.com'),
        license=openapi.License(name='MIT'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    
    # Fauna endpoints (incluye categorías, amenazas, acciones)
    path('api/fauna/', include('apps.fauna.urls')),
    
    # Flora endpoints  
    path('api/flora/', include('apps.flora.urls')),
    
    # Gallery endpoints
    path('api/galeria/', include('apps.galeria.urls')),
    
    # API Documentation
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
