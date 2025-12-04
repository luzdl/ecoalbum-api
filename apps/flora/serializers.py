"""Flora serializers"""
from rest_framework import serializers
from .models import Flora, FotoFlora


class FotoFloraSerializer(serializers.ModelSerializer):
    """Serializer for plant photos"""
    class Meta:
        model = FotoFlora
        fields = ['id', 'url_foto', 'descripcion']


class FloraListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for flora list view"""
    foto_principal = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Flora
        fields = [
            'id',
            'nombre_comun',
            'nombre_cientifico',
            'estado',
            'estado_display',
            'foto_principal'
        ]
    
    def get_foto_principal(self, obj):
        foto = obj.fotos.first()
        return foto.url_foto if foto else None


class FloraMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for cards/thumbnails"""
    foto_principal = serializers.SerializerMethodField()
    
    class Meta:
        model = Flora
        fields = ['id', 'nombre_comun', 'foto_principal']
    
    def get_foto_principal(self, obj):
        foto = obj.fotos.first()
        return foto.url_foto if foto else None


class FloraDetailSerializer(serializers.ModelSerializer):
    """Complete serializer for flora detail view"""
    fotos = FotoFloraSerializer(many=True, read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Flora
        fields = [
            'id',
            'nombre_comun',
            'nombre_cientifico',
            'descripcion',
            'distribucion',
            'estado',
            'estado_display',
            'fotos'
        ]
