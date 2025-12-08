"""Gallery serializers for carousel endpoints"""
from rest_framework import serializers
from apps.fauna.models import FotoAnimal
from apps.flora.models import FotoFlora


class FotoAnimalEditSerializer(serializers.ModelSerializer):
    """Serializer para ver y editar fotos de fauna"""
    animal_nombre = serializers.CharField(source='animal.nombre_comun', read_only=True)
    animal_cientifico = serializers.CharField(source='animal.nombre_cientifico', read_only=True)
    
    class Meta:
        model = FotoAnimal
        fields = ('id_foto', 'animal_id', 'animal_nombre', 'animal_cientifico', 'url_foto', 'descripcion')
        read_only_fields = ('id_foto', 'animal_id', 'animal_nombre', 'animal_cientifico')


class FotoFloraEditSerializer(serializers.ModelSerializer):
    """Serializer para ver y editar fotos de flora"""
    planta_nombre = serializers.CharField(source='planta.nombre_comun', read_only=True)
    planta_cientifico = serializers.CharField(source='planta.nombre_cientifico', read_only=True)
    
    class Meta:
        model = FotoFlora
        fields = ('id_foto', 'planta_id', 'planta_nombre', 'planta_cientifico', 'url_foto', 'descripcion')
        read_only_fields = ('id_foto', 'planta_id', 'planta_nombre', 'planta_cientifico')


class GaleriaItemSerializer(serializers.Serializer):
    """Serializer for gallery items (unified fauna/flora photos)"""
    id = serializers.IntegerField()
    tipo = serializers.CharField()  # 'fauna' or 'flora'
    nombre = serializers.CharField()
    url_foto = serializers.URLField()
    descripcion_foto = serializers.CharField(allow_null=True)
    especie_id = serializers.IntegerField()
    
    # Optional detailed info
    nombre_cientifico = serializers.CharField(required=False)
    estado = serializers.CharField(required=False)
