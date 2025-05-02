from django.contrib import admin
from .models import PQRS

@admin.register(PQRS)
class PQRSAdmin(admin.ModelAdmin):
    list_display = ('referencia', 'usuario', 'tipo', 'estado', 'fecha_creacion')
    list_filter = ('tipo', 'estado')
    search_fields = ('referencia', 'usuario__username', 'descripcion')
    readonly_fields = ('referencia', 'usuario', 'fecha_creacion')

