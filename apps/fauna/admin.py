from django.contrib import admin
from .models import Categoria, Animal, FotoAnimal, Amenaza, AccionProteccion, AnimalAmenaza, AnimalAccionProteccion


class FotoAnimalInline(admin.TabularInline):
    model = FotoAnimal
    extra = 1


class AnimalAmenazaInline(admin.TabularInline):
    model = AnimalAmenaza
    extra = 1


class AnimalAccionProteccionInline(admin.TabularInline):
    model = AnimalAccionProteccion
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['nombre_comun', 'nombre_cientifico', 'categoria', 'estado']
    list_filter = ['categoria', 'estado']
    search_fields = ['nombre_comun', 'nombre_cientifico']
    inlines = [FotoAnimalInline, AnimalAmenazaInline, AnimalAccionProteccionInline]


@admin.register(Amenaza)
class AmenazaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']


@admin.register(AccionProteccion)
class AccionProteccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'descripcion']
    search_fields = ['titulo']
