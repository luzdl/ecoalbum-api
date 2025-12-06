"""Fauna filters"""
from django_filters import rest_framework as filters
from django.db import models
from .models import Animal


class AnimalFilter(filters.FilterSet):
    """Advanced filtering for animals"""
    q = filters.CharFilter(method='search_filter', label='Búsqueda')
    categoria = filters.CharFilter(field_name='categoria__nombre', lookup_expr='iexact')
    estado = filters.ChoiceFilter(choices=Animal.ESTADO_CHOICES)
    letra = filters.CharFilter(method='letra_filter', label='Filtro alfabético')
    
    class Meta:
        model = Animal
        fields = ['q', 'categoria', 'estado', 'letra']
    
    def search_filter(self, queryset, name, value):
        """Search by common name or scientific name"""
        return queryset.filter(
            models.Q(nombre_comun__icontains=value) |
            models.Q(nombre_cientifico__icontains=value)
        )
    
    def letra_filter(self, queryset, name, value):
        """Filter by first letter of common name"""
        if value:
            return queryset.filter(nombre_comun__istartswith=value[0])
        return queryset
