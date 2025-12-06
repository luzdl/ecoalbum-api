"""Fauna models - Alineados con schema.sql"""
from django.db import models


class Categoria(models.Model):
    """Modelo para categorías de animales"""
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=50,
        unique=True,
        choices=[
            ('Aves', 'Aves'),
            ('Mamíferos', 'Mamíferos'),
            ('Reptiles', 'Reptiles'),
            ('Peces marinos', 'Peces marinos'),
            ('Equinodermos', 'Equinodermos'),
            ('Anfibios', 'Anfibios'),
        ]
    )
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre
    
    @property
    def id(self):
        """Alias para compatibilidad con serializers"""
        return self.id_categoria


class Animal(models.Model):
    """Modelo para animales"""
    ESTADO_CHOICES = [
        ('Preocupación menor (LC)', 'Preocupación menor (LC)'),
        ('Casi amenazado (NT)', 'Casi amenazado (NT)'),
        ('Vulnerable (VU)', 'Vulnerable (VU)'),
        ('En peligro (EN)', 'En peligro (EN)'),
        ('Peligro crítico (CR)', 'Peligro crítico (CR)'),
    ]
    
    id_animal = models.AutoField(primary_key=True)
    nombre_comun = models.CharField(max_length=200)
    nombre_cientifico = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    habitat = models.TextField(blank=True, null=True)
    distribucion = models.TextField(blank=True, null=True)
    importancia_ecologica = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='id_categoria',
        related_name='animales'
    )
    amenazas = models.ManyToManyField(
        'Amenaza',
        through='AnimalAmenaza',
        related_name='animales'
    )
    acciones_proteccion = models.ManyToManyField(
        'AccionProteccion',
        through='AnimalAccionProteccion',
        related_name='animales'
    )

    class Meta:
        db_table = 'Animal'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'

    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"
    
    @property
    def id(self):
        """Alias para compatibilidad con serializers"""
        return self.id_animal
    
    def get_estado_display(self):
        """Retorna el estado tal cual (ya es legible)"""
        return self.estado or ''


class FotoAnimal(models.Model):
    """Modelo para fotos de animales"""
    id_foto = models.AutoField(primary_key=True)
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        db_column='id_animal',
        related_name='fotos'
    )
    url_foto = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'FotoAnimal'
        verbose_name = 'Foto de Animal'
        verbose_name_plural = 'Fotos de Animales'

    def __str__(self):
        return f"Foto de {self.animal.nombre_comun}"
    
    @property
    def id(self):
        """Alias para compatibilidad con serializers"""
        return self.id_foto


class Amenaza(models.Model):
    """Modelo para amenazas"""
    id_amenaza = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Amenaza'
        verbose_name = 'Amenaza'
        verbose_name_plural = 'Amenazas'

    def __str__(self):
        return self.nombre
    
    @property
    def id(self):
        """Alias para compatibilidad con serializers"""
        return self.id_amenaza


class AnimalAmenaza(models.Model):
    """Tabla intermedia para la relación Animal-Amenaza"""
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
        verbose_name = 'Animal-Amenaza'
        verbose_name_plural = 'Animal-Amenazas'


class AccionProteccion(models.Model):
    """Modelo para acciones de protección"""
    id_accion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    class Meta:
        db_table = 'AccionProteccion'
        verbose_name = 'Acción de Protección'
        verbose_name_plural = 'Acciones de Protección'

    def __str__(self):
        return self.titulo
    
    @property
    def id(self):
        """Alias para compatibilidad con serializers"""
        return self.id_accion


class AnimalAccionProteccion(models.Model):
    """Tabla intermedia para la relación Animal-AccionProteccion"""
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
        verbose_name = 'Animal-Acción de Protección'
        verbose_name_plural = 'Animal-Acciones de Protección'
