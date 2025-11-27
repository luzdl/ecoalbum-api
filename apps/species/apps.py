"""Species app configuration"""
from django.apps import AppConfig


class SpeciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.species'
    verbose_name = 'Species Catalog'
