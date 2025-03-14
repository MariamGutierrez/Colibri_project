from django import forms
from .models import ReporteMaltrato, Evidencia

class ReporteMaltratoForm(forms.ModelForm):
    class Meta:
        model = ReporteMaltrato
        fields = ['descripcion', 'imagen', 'video', 'audio']


    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get("latitud")
        lng = cleaned_data.get("longitud")

        # Validar que la ubicación está dentro de Colombia
        COLOMBIA_BOUNDS = {
            "minLat": -4.231687, "maxLat": 16.0000,
            "minLng": -81.7281, "maxLng": -66.8519
        }
        if not (COLOMBIA_BOUNDS["minLat"] <= lat <= COLOMBIA_BOUNDS["maxLat"]) or \
           not (COLOMBIA_BOUNDS["minLng"] <= lng <= COLOMBIA_BOUNDS["maxLng"]):
            raise forms.ValidationError("Ubicación fuera de Colombia.")

        return cleaned_data

class EvidenciaForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ['archivo']
