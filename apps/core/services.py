"""Core app services"""
from django.db import connection
from django.utils import timezone


def get_health_status():
    """Get system health status"""
    status = 'healthy'
    message = 'All systems operational'
    database_status = 'unknown'

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            database_status = 'connected'
    except Exception as e:
        status = 'unhealthy'
        message = f'Database error: {str(e)}'
        database_status = 'disconnected'

    return {
        'status': status,
        'database': database_status,
        'timestamp': timezone.now(),
        'message': message
    }
