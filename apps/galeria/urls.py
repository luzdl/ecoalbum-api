"""Gallery URL configuration"""
from django.urls import path
from .views import DestacadosView, AleatoriosView, EstadisticasView

app_name = 'galeria'

urlpatterns = [
    path('destacados/', DestacadosView.as_view(), name='destacados'),
    path('aleatorios/', AleatoriosView.as_view(), name='aleatorios'),
    path('estadisticas/', EstadisticasView.as_view(), name='estadisticas'),
]
