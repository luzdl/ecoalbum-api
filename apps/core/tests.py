"""Core app tests"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class HealthCheckTestCase(TestCase):
    """Test health check endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_health_check_endpoint_exists(self):
        """Test that health check endpoint is accessible"""
        response = self.client.get('/api/health/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE])

    def test_health_check_response_format(self):
        """Test health check response format"""
        response = self.client.get('/api/health/')
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('database', data)
        self.assertIn('timestamp', data)
        self.assertIn('message', data)
