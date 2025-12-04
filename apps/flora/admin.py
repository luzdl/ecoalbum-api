"""Flora admin configuration"""
from django.contrib import admin
from .models import Flora, FotoFlora


class FotoFloraInline(admin.TabularInline):
    """Inline admin for plant photos"""
    model = FotoFlora
    extra = 1
    fields = ['url_foto', 'descripcion']


@admin.register(Flora)
class FloraAdmin(admin.ModelAdmin):
    """Admin configuration for Flora model"""
    list_display = [
        'nombre_comun',
        'nombre_cientifico',
        'estado',
        'get_fotos_count'
    ]
    list_filter = ['estado']
    search_fields = ['nombre_comun', 'nombre_cientifico', 'descripcion']
    ordering = ['nombre_comun']
    inlines = [FotoFloraInline]
    
    fieldsets = (
        ('Identificación', {
            'fields': ('nombre_comun', 'nombre_cientifico')
        }),
        ('Descripción', {
            'fields': ('descripcion', 'distribucion')
        }),
        ('Estado de Conservación', {
            'fields': ('estado',)
        }),
    )
    
    def get_fotos_count(self, obj):
        return obj.fotos.count()
    get_fotos_count.short_description = 'Fotos'


@admin.register(FotoFlora)
class FotoFloraAdmin(admin.ModelAdmin):
    """Admin configuration for plant photos"""
    list_display = ['id', 'planta', 'url_foto', 'descripcion']
    list_filter = ['planta']
    search_fields = ['planta__nombre_comun', 'descripcion']
