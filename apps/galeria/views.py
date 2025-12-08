"""Gallery views for carousel endpoints"""
import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.fauna.models import FotoAnimal, Animal
from apps.flora.models import FotoFlora, Flora
from .serializers import GaleriaItemSerializer, FotoAnimalEditSerializer, FotoFloraEditSerializer


# Estados de conservación (sincronizados con schema.sql)
ESTADO_FAUNA_CHOICES = [
    'Preocupación menor (LC)',
    'Casi amenazado (NT)',
    'Vulnerable (VU)',
    'En peligro (EN)',
    'Peligro crítico (CR)',
]

ESTADO_FLORA_CHOICES = [
    'Preocupación menor (LC)',
    'Vulnerable (VU)',
    'En peligro (EN)',
    'Peligro crítico (CR)',
]


class FotoAnimalDetailUpdateView(RetrieveUpdateAPIView):
    """
    GET: Ver detalle de una foto de fauna por ID del animal.
    PATCH/PUT: Editar url_foto y descripcion (requiere autenticación).
    """
    queryset = FotoAnimal.objects.select_related('animal')
    serializer_class = FotoAnimalEditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'animal_id'
    lookup_url_kwarg = 'id_animal'
    
    @swagger_auto_schema(
        operation_description="Obtener detalle de la foto de un animal por su ID",
        responses={200: FotoAnimalEditSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar url_foto y/o descripcion de la foto de un animal (requiere autenticación)",
        request_body=FotoAnimalEditSerializer,
        responses={200: FotoAnimalEditSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar foto de fauna completa por ID del animal (requiere autenticación)",
        request_body=FotoAnimalEditSerializer,
        responses={200: FotoAnimalEditSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class FotoFloraDetailUpdateView(RetrieveUpdateAPIView):
    """
    GET: Ver detalle de una foto de flora por ID de la planta.
    PATCH/PUT: Editar url_foto y descripcion (requiere autenticación).
    """
    queryset = FotoFlora.objects.select_related('planta')
    serializer_class = FotoFloraEditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'planta_id'
    lookup_url_kwarg = 'id_planta'
    
    @swagger_auto_schema(
        operation_description="Obtener detalle de la foto de una planta por su ID",
        responses={200: FotoFloraEditSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar url_foto y/o descripcion de la foto de una planta (requiere autenticación)",
        request_body=FotoFloraEditSerializer,
        responses={200: FotoFloraEditSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class EstadosConservacionView(APIView):
    """
    Obtener lista de estados de conservación disponibles.
    Separados por tipo (fauna tiene más opciones que flora según el schema).
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Obtener lista de estados de conservación disponibles",
        responses={
            200: openapi.Response(
                description="Estados de conservación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'fauna': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        ),
                        'flora': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            )
        }
    )
    def get(self, request):
        return Response({
            'fauna': ESTADO_FAUNA_CHOICES,
            'flora': ESTADO_FLORA_CHOICES,
        })


class DestacadosView(APIView):
    """
    Get featured photos for homepage carousel.
    Returns a curated selection of photos from both fauna and flora.
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Get featured photos for homepage carousel",
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of photos to return (default: 10, max: 20)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'tipo',
                openapi.IN_QUERY,
                description="Filter by type: 'fauna', 'flora', or 'todos' (default)",
                type=openapi.TYPE_STRING,
                enum=['fauna', 'flora', 'todos']
            )
        ],
        responses={200: GaleriaItemSerializer(many=True)}
    )
    def get(self, request):
        """Get featured photos"""
        limit = min(int(request.query_params.get('limit', 10)), 20)
        tipo = request.query_params.get('tipo', 'todos')
        
        items = []
        
        # Get fauna photos
        if tipo in ['fauna', 'todos']:
            fauna_fotos = FotoAnimal.objects.select_related('animal', 'animal__categoria')[:limit]
            for foto in fauna_fotos:
                items.append({
                    'id': foto.id_foto,
                    'tipo': 'fauna',
                    'nombre': foto.animal.nombre_comun,
                    'url_foto': foto.url_foto,
                    'descripcion_foto': foto.descripcion,
                    'especie_id': foto.animal.id_animal,
                    'nombre_cientifico': foto.animal.nombre_cientifico,
                    'estado': foto.animal.estado
                })
        
        # Get flora photos
        if tipo in ['flora', 'todos']:
            flora_fotos = FotoFlora.objects.select_related('planta')[:limit]
            for foto in flora_fotos:
                items.append({
                    'id': foto.id_foto,
                    'tipo': 'flora',
                    'nombre': foto.planta.nombre_comun,
                    'url_foto': foto.url_foto,
                    'descripcion_foto': foto.descripcion,
                    'especie_id': foto.planta.id_planta,
                    'nombre_cientifico': foto.planta.nombre_cientifico,
                    'estado': foto.planta.estado
                })
        
        # Limit total results
        items = items[:limit]
        
        serializer = GaleriaItemSerializer(items, many=True)
        return Response(serializer.data)


class AleatoriosView(APIView):
    """
    Get random photos for dynamic content display.
    Returns randomly selected photos from fauna and flora.
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Get random photos for dynamic content",
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of photos to return (default: 10, max: 20)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'tipo',
                openapi.IN_QUERY,
                description="Filter by type: 'fauna', 'flora', or 'todos' (default)",
                type=openapi.TYPE_STRING,
                enum=['fauna', 'flora', 'todos']
            )
        ],
        responses={200: GaleriaItemSerializer(many=True)}
    )
    def get(self, request):
        """Get random photos"""
        limit = min(int(request.query_params.get('limit', 10)), 20)
        tipo = request.query_params.get('tipo', 'todos')
        
        items = []
        half_limit = limit // 2
        
        # Get random fauna photos
        if tipo in ['fauna', 'todos']:
            fauna_count = FotoAnimal.objects.count()
            if fauna_count > 0:
                # Use random IDs for better performance than ORDER BY RAND()
                fauna_limit = limit if tipo == 'fauna' else half_limit
                fauna_ids = list(FotoAnimal.objects.values_list('id_foto', flat=True))
                random_fauna_ids = random.sample(fauna_ids, min(fauna_limit, len(fauna_ids)))
                
                fauna_fotos = FotoAnimal.objects.filter(
                    id_foto__in=random_fauna_ids
                ).select_related('animal', 'animal__categoria')
                
                for foto in fauna_fotos:
                    items.append({
                        'id': foto.id_foto,
                        'tipo': 'fauna',
                        'nombre': foto.animal.nombre_comun,
                        'url_foto': foto.url_foto,
                        'descripcion_foto': foto.descripcion,
                        'especie_id': foto.animal.id_animal,
                        'nombre_cientifico': foto.animal.nombre_cientifico,
                        'estado': foto.animal.estado
                    })
        
        # Get random flora photos
        if tipo in ['flora', 'todos']:
            flora_count = FotoFlora.objects.count()
            if flora_count > 0:
                flora_limit = limit if tipo == 'flora' else half_limit
                flora_ids = list(FotoFlora.objects.values_list('id_foto', flat=True))
                random_flora_ids = random.sample(flora_ids, min(flora_limit, len(flora_ids)))
                
                flora_fotos = FotoFlora.objects.filter(
                    id_foto__in=random_flora_ids
                ).select_related('planta')
                
                for foto in flora_fotos:
                    items.append({
                        'id': foto.id_foto,
                        'tipo': 'flora',
                        'nombre': foto.planta.nombre_comun,
                        'url_foto': foto.url_foto,
                        'descripcion_foto': foto.descripcion,
                        'especie_id': foto.planta.id_planta,
                        'nombre_cientifico': foto.planta.nombre_cientifico,
                        'estado': foto.planta.estado
                    })
        
        # Shuffle results for mixed display
        if tipo == 'todos':
            random.shuffle(items)
        
        serializer = GaleriaItemSerializer(items, many=True)
        return Response(serializer.data)


class EstadisticasView(APIView):
    """
    Get statistics for the gallery/homepage.
    Returns counts of animals, plants, and photos.
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Get gallery statistics",
        responses={
            200: openapi.Response(
                description="Gallery statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_animales': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_plantas': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_fotos_fauna': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_fotos_flora': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_especies': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_fotos': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            )
        }
    )
    def get(self, request):
        """Get gallery statistics"""
        total_animales = Animal.objects.count()
        total_plantas = Flora.objects.count()
        total_fotos_fauna = FotoAnimal.objects.count()
        total_fotos_flora = FotoFlora.objects.count()
        
        return Response({
            'total_animales': total_animales,
            'total_plantas': total_plantas,
            'total_fotos_fauna': total_fotos_fauna,
            'total_fotos_flora': total_fotos_flora,
            'total_especies': total_animales + total_plantas,
            'total_fotos': total_fotos_fauna + total_fotos_flora
        })
