"""Flora models - Alineados con schema.sql"""
from django.db import models


class Flora(models.Model):
    """Modelo para plantas"""
    ESTADO_CHOICES = [
        ('Preocupación menor (LC)', 'Preocupación menor (LC)'),
        ('Vulnerable (VU)', 'Vulnerable (VU)'),
        ('En peligro (EN)', 'En peligro (EN)'),
        ('Peligro crítico (CR)', 'Peligro crítico (CR)'),
    ]
    
    id_planta = models.AutoField(primary_key=True)
    nombre_comun = models.CharField(max_length=200)
    nombre_cientifico = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    distribucion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, blank=True, null=True)

    class Meta:
        db_table = 'Flora'
        verbose_name = 'Flora'
        verbose_name_plural = 'Flora'

    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"
    
    @property
    def id(self):
        """Alias para compatibilidad con serializers"""
        return self.id_planta
    
    def get_estado_display(self):
        """Retorna el estado tal cual (ya es legible)"""
        return self.estado or ''


class FotoFlora(models.Model):
    """Modelo para fotos de plantas"""
    id_foto = models.AutoField(primary_key=True)
    planta = models.ForeignKey(
        Flora,
        on_delete=models.CASCADE,
        db_column='id_planta',
        related_name='fotos'
    )
    url_foto = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'FotoFlora'
        verbose_name = 'Foto de Flora'
        verbose_name_plural = 'Fotos de Flora'

    def __str__(self):
        return f"Foto de {self.planta.nombre_comun}"
    
    @property
    def id(self):
        """Alias para compatibilidad con serializers"""
        return self.id_foto
