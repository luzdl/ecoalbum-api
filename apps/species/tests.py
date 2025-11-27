"""Species app tests"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Species


class CategoryTestCase(TestCase):
    """Test Category model and endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Mammals',
            description='Mammalian species'
        )

    def test_category_creation(self):
        """Test category creation"""
        self.assertEqual(self.category.name, 'Mammals')
        self.assertTrue(self.category.id)

    def test_category_list_endpoint(self):
        """Test category list endpoint"""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreater(len(data['results']), 0)


class SpeciesTestCase(TestCase):
    """Test Species model and endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Birds',
            description='Avian species'
        )
        self.species = Species.objects.create(
            common_name='Harpy Eagle',
            scientific_name='Harpia harpyja',
            category=self.category,
            endemic=True,
            risk_level='VU'
        )

    def test_species_creation(self):
        """Test species creation"""
        self.assertEqual(self.species.common_name, 'Harpy Eagle')
        self.assertTrue(self.species.endemic)

    def test_species_list_endpoint(self):
        """Test species list endpoint"""
        response = self.client.get('/api/species/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_species_detail_endpoint(self):
        """Test species detail endpoint"""
        response = self.client.get(f'/api/species/{self.species.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['scientific_name'], 'Harpia harpyja')
