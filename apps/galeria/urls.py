"""Gallery URL configuration"""
from django.urls import path
from .views import (
    DestacadosView, 
    AleatoriosView, 
    EstadisticasView,
    FotoAnimalDetailUpdateView,
    FotoFloraDetailUpdateView,
    EstadosConservacionView,
)

app_name = 'galeria'

urlpatterns = [
    # Carousel endpoints
    path('destacados/', DestacadosView.as_view(), name='destacados'),
    path('aleatorios/', AleatoriosView.as_view(), name='aleatorios'),
    path('estadisticas/', EstadisticasView.as_view(), name='estadisticas'),
    
    # Foto edit endpoints (GET público, PATCH requiere auth) - por ID de animal/planta
    path('fotos/fauna/<int:id_animal>/', FotoAnimalDetailUpdateView.as_view(), name='foto-fauna-detail'),
    path('fotos/flora/<int:id_planta>/', FotoFloraDetailUpdateView.as_view(), name='foto-flora-detail'),
    
    # Estados de conservación
    path('estados-conservacion/', EstadosConservacionView.as_view(), name='estados-conservacion'),
]
