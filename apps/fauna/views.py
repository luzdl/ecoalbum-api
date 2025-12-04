"""Fauna views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Categoria, Animal, FotoAnimal, Amenaza, AccionProteccion
from .serializers import (
    CategoriaSerializer,
    AnimalListSerializer,
    AnimalMinimalSerializer,
    AnimalDetailSerializer,
    FotoAnimalSerializer,
    AmenazaSerializer,
    AccionProteccionSerializer
)
from .filters import AnimalFilter


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for animal categories"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    

class AnimalViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for fauna/animals with dynamic field selection"""
    queryset = Animal.objects.select_related('categoria').prefetch_related('fotos', 'amenazas', 'acciones_proteccion')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AnimalFilter
    ordering_fields = ['nombre_comun', 'nombre_cientifico', 'estado', 'id']
    ordering = ['nombre_comun']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action and query params"""
        if self.action == 'retrieve':
            return AnimalDetailSerializer
        
        # Check for fields parameter for sparse fieldsets
        fields = self.request.query_params.get('fields')
        if fields:
            # Return minimal or list based on requested fields
            field_list = fields.split(',')
            if len(field_list) <= 3:
                return AnimalMinimalSerializer
        
        return AnimalListSerializer
    
    @action(detail=True, methods=['get'])
    def fotos(self, request, pk=None):
        """Get all photos for an animal"""
        animal = self.get_object()
        fotos = animal.fotos.all()
        serializer = FotoAnimalSerializer(fotos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def amenazas(self, request, pk=None):
        """Get all threats for an animal"""
        animal = self.get_object()
        amenazas = animal.amenazas.all()
        serializer = AmenazaSerializer(amenazas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def acciones(self, request, pk=None):
        """Get all protection actions for an animal"""
        animal = self.get_object()
        acciones = animal.acciones_proteccion.all()
        serializer = AccionProteccionSerializer(acciones, many=True)
        return Response(serializer.data)


class AmenazaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for threats"""
    queryset = Amenaza.objects.all()
    serializer_class = AmenazaSerializer
    permission_classes = [AllowAny]


class AccionProteccionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for protection actions"""
    queryset = AccionProteccion.objects.all()
    serializer_class = AccionProteccionSerializer
    permission_classes = [AllowAny]
