from django import forms
from .models import PQRS

class PQRSForm(forms.ModelForm):
    class Meta:
        model = PQRS
        fields = ['tipo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
