"""Species serializer"""
from rest_framework import serializers
from ..models import Species, Category


class SpeciesListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Species list view"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    cites_status_display = serializers.CharField(source='get_cites_status_display', read_only=True)

    class Meta:
        model = Species
        fields = [
            'id',
            'common_name',
            'scientific_name',
            'category',
            'category_name',
            'risk_level',
            'risk_level_display',
            'cites_status',
            'cites_status_display',
            'endemic',
            'image_url',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SpeciesDetailSerializer(serializers.ModelSerializer):
    """Full serializer for Species detail view"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    cites_status_display = serializers.CharField(source='get_cites_status_display', read_only=True)

    class Meta:
        model = Species
        fields = [
            'id',
            'common_name',
            'scientific_name',
            'category',
            'category_id',
            'risk_level',
            'risk_level_display',
            'cites_status',
            'cites_status_display',
            'image_url',
            'description',
            'endemic',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
