"""Species filtering"""
from django_filters import rest_framework as filters
from ..models import Species


class SpeciesFilter(filters.FilterSet):
    """Filter for Species with search and advanced filtering"""
    q = filters.CharFilter(
        field_name='common_name',
        lookup_expr='icontains',
        label='Search by common name or scientific name'
    )
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    risk_level = filters.ChoiceFilter(choices=Species._meta.get_field('risk_level').choices)
    endemic = filters.BooleanFilter()

    class Meta:
        model = Species
        fields = ['q', 'category', 'risk_level', 'endemic']
