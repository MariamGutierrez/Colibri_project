from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import PerfilONG

class RegistroVisitanteForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            visitante_group, _ = Group.objects.get_or_create(name='Visitantes')
            user.groups.add(visitante_group)
        return user

class RegistroONGForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre_organizacion = forms.CharField(max_length=255, required=True)
    descripcion = forms.CharField(widget=forms.Textarea, required=True)
    sitio_web = forms.URLField(required=False)
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=255, required=False)
    fecha_fundacion = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    area_enfoque = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Simplemente asignar al grupo ONGs
            ong_group = Group.objects.get(name='ONGs')
            user.groups.add(ong_group)
            
            # Crear perfil de ONG
            PerfilONG.objects.create(
                usuario=user,
                nombre_organizacion=self.cleaned_data['nombre_organizacion'],
                descripcion=self.cleaned_data['descripcion'],
                sitio_web=self.cleaned_data['sitio_web'],
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion'],
                fecha_fundacion=self.cleaned_data['fecha_fundacion'],
                area_enfoque=self.cleaned_data['area_enfoque']
            )
        return user