from django.contrib import admin
from .models import Avistamiento, ImagenAvistamiento
from django.utils.html import format_html

@admin.register(Avistamiento)
class AvistamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'publicado')
    list_filter = ('publicado',)
    actions = ['aprobar_avistamientos']

    def aprobar_avistamientos(self, request, queryset):
        queryset.update(publicado=True)
    aprobar_avistamientos.short_description = "Aprobar avistamientos seleccionados"

class ImagenAvistamientoAdmin(admin.ModelAdmin):
    list_display = ('avistamiento', 'preview')  # Agregar la vista previa

    def preview(self, obj):
        if obj.imagen:  # Verifica si hay imagen
            return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/>', obj.imagen.url)
        return "(No image)"

    preview.allow_tags = True
    preview.short_description = "Vista previa"

admin.site.register(ImagenAvistamiento, ImagenAvistamientoAdmin)
