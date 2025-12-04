"""Flora views - ViewSets for plant endpoints"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Flora, FotoFlora
from .serializers import (
    FloraListSerializer,
    FloraDetailSerializer,
    FloraMinimalSerializer,
    FotoFloraSerializer
)
from .filters import FloraFilter


class FloraViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Flora (plants) CRUD operations.
    
    list:
        Get all plants with optional filtering.
        
    retrieve:
        Get a single plant by ID with full details.
        
    fotos:
        Get all photos for a specific plant.
    """
    queryset = Flora.objects.prefetch_related('fotos')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FloraFilter
    ordering_fields = ['nombre_comun', 'nombre_cientifico', 'estado']
    ordering = ['nombre_comun']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            # Check for 'minimal' query param for card views
            if self.request.query_params.get('minimal') == 'true':
                return FloraMinimalSerializer
            return FloraListSerializer
        return FloraDetailSerializer
    
    def get_queryset(self):
        """Optimize queryset based on action"""
        queryset = super().get_queryset()
        
        # For list, we only need the first photo
        if self.action == 'list':
            queryset = queryset.prefetch_related('fotos')
        
        return queryset
    
    @swagger_auto_schema(
        operation_description="Get all photos for a specific plant",
        responses={200: FotoFloraSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def fotos(self, request, pk=None):
        """Get all photos for a plant"""
        planta = self.get_object()
        fotos = planta.fotos.all()
        serializer = FotoFloraSerializer(fotos, many=True)
        return Response(serializer.data)
