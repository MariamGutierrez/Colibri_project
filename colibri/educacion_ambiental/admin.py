from django.contrib import admin
from .models import Articulo, ImagenArticulo, VideoArticulo

class ImagenArticuloInline(admin.TabularInline):
    model = ImagenArticulo
    extra = 1

class VideoArticuloInline(admin.TabularInline):
    model = VideoArticulo
    extra = 1

class ArticuloAdmin(admin.ModelAdmin):
    inlines = [ImagenArticuloInline, VideoArticuloInline]
    list_display = ('titulo', 'categoria', 'region', 'fecha_publicacion', 'publish')  # Agregar 'region'
    search_fields = ('titulo', 'contenido')
    list_filter = ('categoria', 'region', 'fecha_publicacion', 'publish')  # Agregar 'region'

admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(ImagenArticulo)
admin.site.register(VideoArticulo)