from django.contrib import admin
from .models import TipoReporte, Reporte  # Reemplaza con los modelos que has creado

admin.site.register(Reporte)
admin.site.register(TipoReporte)
