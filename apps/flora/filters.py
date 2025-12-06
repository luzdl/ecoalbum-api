"""Flora filters for advanced querying"""
import django_filters
from django.db import models
from .models import Flora


class FloraFilter(django_filters.FilterSet):
    """Filter for Flora queryset"""
    
    # Text search across multiple fields
    q = django_filters.CharFilter(method='search_filter', label='Búsqueda general')
    
    # Filter by conservation status
    estado = django_filters.ChoiceFilter(
        choices=Flora.ESTADO_CHOICES,
        label='Estado de conservación'
    )
    
    # Filter by first letter of common name
    letra = django_filters.CharFilter(
        method='filter_by_letter',
        label='Filtrar por letra inicial'
    )
    
    class Meta:
        model = Flora
        fields = ['estado', 'q', 'letra']
    
    def search_filter(self, queryset, name, value):
        """Search across common name, scientific name, and description"""
        return queryset.filter(
            models.Q(nombre_comun__icontains=value) |
            models.Q(nombre_cientifico__icontains=value) |
            models.Q(descripcion__icontains=value)
        )
    
    def filter_by_letter(self, queryset, name, value):
        """Filter plants by first letter of common name"""
        if value and len(value) == 1:
            return queryset.filter(nombre_comun__istartswith=value)
        return queryset
