"""Category views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Category
from ..serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering = ['name']
