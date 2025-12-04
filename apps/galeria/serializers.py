"""Gallery serializers for carousel endpoints"""
from rest_framework import serializers


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
