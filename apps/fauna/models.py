"""Fauna models - Animals, Categories, Photos, Threats, Protection Actions"""
from django.db import models


class EstadoConservacion(models.TextChoices):
    """IUCN Conservation status choices"""
    LC = 'LC', 'Preocupación menor (LC)'
    NT = 'NT', 'Casi amenazado (NT)'
    VU = 'VU', 'Vulnerable (VU)'
    EN = 'EN', 'En peligro (EN)'
    CR = 'CR', 'Peligro crítico (CR)'


class Categoria(models.Model):
    """Animal category model"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'Categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Amenaza(models.Model):
    """Threat model"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'Amenaza'
        verbose_name = 'Amenaza'
        verbose_name_plural = 'Amenazas'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class AccionProteccion(models.Model):
    """Protection action model"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    class Meta:
        db_table = 'AccionProteccion'
        verbose_name = 'Acción de Protección'
        verbose_name_plural = 'Acciones de Protección'
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo


class Animal(models.Model):
    """Main fauna/animal model"""
    nombre_comun = models.CharField(max_length=200)
    nombre_cientifico = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    habitat = models.TextField(blank=True, null=True)
    distribucion = models.TextField(blank=True, null=True)
    importancia_ecologica = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=50,
        choices=EstadoConservacion.choices,
        default=EstadoConservacion.LC
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='animales',
        db_column='id_categoria'
    )
    amenazas = models.ManyToManyField(
        Amenaza,
        through='AnimalAmenaza',
        related_name='animales'
    )
    acciones_proteccion = models.ManyToManyField(
        AccionProteccion,
        through='AnimalAccionProteccion',
        related_name='animales'
    )
    
    class Meta:
        db_table = 'Animal'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'
        ordering = ['nombre_comun']
        indexes = [
            models.Index(fields=['nombre_comun']),
            models.Index(fields=['nombre_cientifico']),
            models.Index(fields=['estado']),
            models.Index(fields=['categoria']),
        ]
    
    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"
    
    @property
    def foto_principal(self):
        """Get the first photo as main photo"""
        foto = self.fotos.first()
        return foto.url_foto if foto else None


class FotoAnimal(models.Model):
    """Animal photo model"""
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='fotos',
        db_column='id_animal'
    )
    url_foto = models.URLField(max_length=500)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'FotoAnimal'
        verbose_name = 'Foto de Animal'
        verbose_name_plural = 'Fotos de Animales'
    
    def __str__(self):
        return f"Foto de {self.animal.nombre_comun}"


class AnimalAmenaza(models.Model):
    """Animal-Threat junction table"""
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        db_column='id_animal'
    )
    amenaza = models.ForeignKey(
        Amenaza,
        on_delete=models.CASCADE,
        db_column='id_amenaza'
    )
    
    class Meta:
        db_table = 'AnimalAmenaza'
        unique_together = ('animal', 'amenaza')
        verbose_name = 'Amenaza de Animal'
        verbose_name_plural = 'Amenazas de Animales'


class AnimalAccionProteccion(models.Model):
    """Animal-Protection Action junction table"""
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        db_column='id_animal'
    )
    accion = models.ForeignKey(
        AccionProteccion,
        on_delete=models.CASCADE,
        db_column='id_accion'
    )
    
    class Meta:
        db_table = 'AnimalAccionProteccion'
        unique_together = ('animal', 'accion')
        verbose_name = 'Acción de Protección de Animal'
        verbose_name_plural = 'Acciones de Protección de Animales'
