from django import forms
from .models import Avistamiento, ImagenAvistamiento

class AvistamientoForm(forms.ModelForm):
    class Meta:
        model = Avistamiento
        fields = ['nombre', 'descripcion', 'latitud', 'longitud', 'tipo_especie', 'estado_conservacion']

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get("latitud")
        lng = cleaned_data.get("longitud")

        COLOMBIA_BOUNDS = {
            "minLat": -4.231687,  # Sur (Leticia)
            "maxLat": 16.0000,    # Norte (Mar Caribe)
            "minLng": -81.7281,   # Oeste (Islas de Colombia)
            "maxLng": -66.8519    # Este (Frontera con Venezuela)
        }

        if not (COLOMBIA_BOUNDS["minLat"] <= lat <= COLOMBIA_BOUNDS["maxLat"]) or \
           not (COLOMBIA_BOUNDS["minLng"] <= lng <= COLOMBIA_BOUNDS["maxLng"]):
            raise forms.ValidationError("La ubicación seleccionada está fuera de Colombia.")

        return cleaned_data

class ImagenAvistamientoForm(forms.ModelForm):
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            ext = imagen.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Solo se permiten imágenes en formato JPG y PNG.")
        return imagen

    class Meta:
        model = ImagenAvistamiento
        fields = ['imagen']




