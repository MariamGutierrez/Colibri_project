from django import forms
from .models import Avistamiento, ImagenAvistamiento

class AvistamientoForm(forms.ModelForm):
    class Meta:
        model = Avistamiento
        fields = ['nombre', 'descripcion', 'latitud', 'longitud']

class ImagenAvistamientoForm(forms.ModelForm):
    class Meta:
        model = ImagenAvistamiento
        fields = ['imagen']

ImagenAvistamientoFormSet = forms.inlineformset_factory(
    Avistamiento, ImagenAvistamiento, form=ImagenAvistamientoForm, extra=3
)




