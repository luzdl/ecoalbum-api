"""Fauna serializers"""
from rest_framework import serializers
from .models import Categoria, Animal, FotoAnimal, Amenaza, AccionProteccion


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer for Categoria"""
    cantidad_animales = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'cantidad_animales']
    
    def get_cantidad_animales(self, obj):
        return obj.animales.count()


class FotoAnimalSerializer(serializers.ModelSerializer):
    """Serializer for animal photos"""
    class Meta:
        model = FotoAnimal
        fields = ['id', 'url_foto', 'descripcion']


class AmenazaSerializer(serializers.ModelSerializer):
    """Serializer for threats"""
    class Meta:
        model = Amenaza
        fields = ['id', 'nombre', 'descripcion']


class AccionProteccionSerializer(serializers.ModelSerializer):
    """Serializer for protection actions"""
    class Meta:
        model = AccionProteccion
        fields = ['id', 'titulo', 'descripcion']


class AnimalListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for animal list view"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    foto_principal = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Animal
        fields = [
            'id',
            'nombre_comun',
            'nombre_cientifico',
            'estado',
            'estado_display',
            'categoria',
            'categoria_nombre',
            'foto_principal'
        ]
    
    def get_foto_principal(self, obj):
        foto = obj.fotos.first()
        return foto.url_foto if foto else None


class AnimalMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for cards/thumbnails"""
    foto_principal = serializers.SerializerMethodField()
    
    class Meta:
        model = Animal
        fields = ['id', 'nombre_comun', 'foto_principal']
    
    def get_foto_principal(self, obj):
        foto = obj.fotos.first()
        return foto.url_foto if foto else None


class AnimalDetailSerializer(serializers.ModelSerializer):
    """Complete serializer for animal detail view"""
    categoria = CategoriaSerializer(read_only=True)
    fotos = FotoAnimalSerializer(many=True, read_only=True)
    amenazas = AmenazaSerializer(many=True, read_only=True)
    acciones_proteccion = AccionProteccionSerializer(many=True, read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Animal
        fields = [
            'id',
            'nombre_comun',
            'nombre_cientifico',
            'descripcion',
            'habitat',
            'distribucion',
            'importancia_ecologica',
            'estado',
            'estado_display',
            'categoria',
            'fotos',
            'amenazas',
            'acciones_proteccion'
        ]


class AnimalDynamicSerializer(serializers.ModelSerializer):
    """Dynamic serializer that accepts fields parameter"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    foto_principal = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    fotos = FotoAnimalSerializer(many=True, read_only=True)
    amenazas = AmenazaSerializer(many=True, read_only=True)
    acciones_proteccion = AccionProteccionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Animal
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        # Get fields from context
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        
        if fields is not None:
            allowed = set(fields.split(','))
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    def get_foto_principal(self, obj):
        foto = obj.fotos.first()
        return foto.url_foto if foto else None
