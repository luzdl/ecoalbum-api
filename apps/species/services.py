"""Species services"""
from django.db.models import Q
from ..models import Species, Category


def get_species_by_category(category_id):
    """Get all species for a category"""
    return Species.objects.filter(category_id=category_id).select_related('category')


def search_species(query):
    """Search species by common or scientific name"""
    return Species.objects.filter(
        Q(common_name__icontains=query) |
        Q(scientific_name__icontains=query)
    ).select_related('category')


def get_endangered_species():
    """Get all endangered species"""
    endangered_status = ['CR', 'EN', 'VU']
    return Species.objects.filter(
        risk_level__in=endangered_status
    ).select_related('category')


def get_endemic_species():
    """Get endemic species"""
    return Species.objects.filter(endemic=True).select_related('category')
