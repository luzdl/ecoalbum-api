"""Flora views"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Flora, FotoFlora
from .serializers import (
    FloraListSerializer,
    FloraDetailSerializer,
    FloraMinimalSerializer,
    FotoFloraSerializer
)
from .filters import FloraFilter


class FloraViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Flora (plants) - Read Only"""
    queryset = Flora.objects.prefetch_related('fotos')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FloraFilter
    ordering_fields = ['nombre_comun', 'nombre_cientifico', 'estado']
    ordering = ['nombre_comun']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return FloraDetailSerializer
        
        # Check for 'minimal' query param for card views
        if self.request.query_params.get('minimal') == 'true':
            return FloraMinimalSerializer
        return FloraListSerializer
    
    @action(detail=True, methods=['get'])
    def fotos(self, request, pk=None):
        """Get all photos for a plant"""
        planta = self.get_object()
        fotos = planta.fotos.all()
        serializer = FotoFloraSerializer(fotos, many=True)
        return Response(serializer.data)
