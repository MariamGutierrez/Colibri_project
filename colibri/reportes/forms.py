from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['tipo_reporte', 'descripcion', 'ubicacion', 'imagen', 'video', 'audio', 'latitud', 'longitud']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
