"""Species views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Species
from ..serializers import SpeciesListSerializer, SpeciesDetailSerializer
from .filters import SpeciesFilter


class SpeciesViewSet(viewsets.ModelViewSet):
    """ViewSet for Species with filtering and search"""
    queryset = Species.objects.select_related('category')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = SpeciesFilter
    search_fields = ['common_name', 'scientific_name', 'description']
    ordering_fields = ['common_name', 'scientific_name', 'created_at', 'risk_level']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return SpeciesDetailSerializer
        return SpeciesListSerializer
