"""Core app views"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HealthCheckSerializer
from .services import get_health_status


class HealthCheckView(APIView):
    """Health check endpoint"""

    def get(self, request):
        """Check API and database health"""
        health_data = get_health_status()
        serializer = HealthCheckSerializer(health_data)
        status_code = status.HTTP_200_OK if health_data['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(serializer.data, status=status_code)
