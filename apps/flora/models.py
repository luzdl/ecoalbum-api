"""Flora models - Plants and Photos"""
from django.db import models


class EstadoConservacionFlora(models.TextChoices):
    """Conservation status choices for flora"""
    LC = 'LC', 'Preocupación menor (LC)'
    VU = 'VU', 'Vulnerable (VU)'
    EN = 'EN', 'En peligro (EN)'
    CR = 'CR', 'Peligro crítico (CR)'


class Flora(models.Model):
    """Plant/Flora model"""
    nombre_comun = models.CharField(max_length=200)
    nombre_cientifico = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    distribucion = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=50,
        choices=EstadoConservacionFlora.choices,
        default=EstadoConservacionFlora.LC
    )
    
    class Meta:
        db_table = 'Flora'
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'
        ordering = ['nombre_comun']
        indexes = [
            models.Index(fields=['nombre_comun']),
            models.Index(fields=['nombre_cientifico']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"
    
    @property
    def foto_principal(self):
        """Get the first photo as main photo"""
        foto = self.fotos.first()
        return foto.url_foto if foto else None


class FotoFlora(models.Model):
    """Plant photo model"""
    planta = models.ForeignKey(
        Flora,
        on_delete=models.CASCADE,
        related_name='fotos',
        db_column='id_planta'
    )
    url_foto = models.URLField(max_length=500)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'FotoFlora'
        verbose_name = 'Foto de Planta'
        verbose_name_plural = 'Fotos de Plantas'
    
    def __str__(self):
        return f"Foto de {self.planta.nombre_comun}"
