from django.contrib import admin
from .models import ReporteMaltrato, Evidencia  # Importar el modelo correcto

admin.site.register(ReporteMaltrato)
admin.site.register(Evidencia)
