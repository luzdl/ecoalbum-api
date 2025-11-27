"""Species model"""
from django.db import models
from .category import Category


class RiskLevel(models.TextChoices):
    """IUCN Red List risk levels"""
    EXTINCT = 'EX', 'Extinct'
    EXTINCT_WILD = 'EW', 'Extinct in the Wild'
    CRITICALLY_ENDANGERED = 'CR', 'Critically Endangered'
    ENDANGERED = 'EN', 'Endangered'
    VULNERABLE = 'VU', 'Vulnerable'
    NEAR_THREATENED = 'NT', 'Near Threatened'
    LEAST_CONCERN = 'LC', 'Least Concern'
    DATA_DEFICIENT = 'DD', 'Data Deficient'
    NOT_EVALUATED = 'NE', 'Not Evaluated'


class CITESStatus(models.TextChoices):
    """CITES status"""
    APPENDIX_I = 'I', 'Appendix I'
    APPENDIX_II = 'II', 'Appendix II'
    APPENDIX_III = 'III', 'Appendix III'
    NOT_LISTED = 'NL', 'Not Listed'


class Species(models.Model):
    """Species model for fauna and flora"""
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='species')
    risk_level = models.CharField(
        max_length=2,
        choices=RiskLevel.choices,
        default=RiskLevel.NOT_EVALUATED
    )
    cites_status = models.CharField(
        max_length=2,
        choices=CITESStatus.choices,
        default=CITESStatus.NOT_LISTED
    )
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    endemic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'species_species'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['endemic']),
            models.Index(fields=['common_name']),
        ]

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"
