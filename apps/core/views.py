"""Core views - Health check"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.utils import timezone


class HealthCheckView(APIView):
    """Health check endpoint"""
    
    def get(self, request):
        """Check API and database health"""
        db_status = 'disconnected'
        api_status = 'unhealthy'
        message = 'Database connection failed'
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = 'connected'
            api_status = 'healthy'
            message = 'All systems operational'
        except Exception as e:
            message = f'Database error: {str(e)}'
        
        data = {
            'status': api_status,
            'database': db_status,
            'timestamp': timezone.now(),
            'message': message
        }
        
        status_code = status.HTTP_200_OK if api_status == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(data, status=status_code)
