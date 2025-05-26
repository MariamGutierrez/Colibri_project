from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegistroVisitanteForm(forms.ModelForm):
    acepta_terminos = forms.BooleanField(
        required=True,
        label="He leído y acepto los Términos y Condiciones",
        widget=forms.CheckboxInput(attrs={'required': True})
    )

    class Meta:
        model = User  # o el modelo de usuario que estés usando
        fields = ['username', 'email', 'password']  # más campos si los usas

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acepta_terminos'].label_suffix = ''  # elimina ":" después del label
