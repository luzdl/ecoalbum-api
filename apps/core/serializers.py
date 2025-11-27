"""Core app serializers"""
from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    """Serializer for health check response"""
    status = serializers.CharField()
    database = serializers.CharField()
    timestamp = serializers.DateTimeField()
    message = serializers.CharField()
