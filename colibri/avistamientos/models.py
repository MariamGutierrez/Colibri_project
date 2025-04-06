from django.db import models
import requests
import os
from django.contrib.auth.models import User
# from apps.avistamientos.views import identificar_especie  # Esto causa un error de importación circular
from avistamientos.utils import identificar_especie 
from django.core.exceptions import ValidationError
def validar_extension_imagen(value):
    ext = value.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('Solo se permiten imágenes en formato JPG y PNG.')

class Avistamiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    TIPO_ESPECIE_CHOICES = [
        ('fauna', 'Fauna'),
        ('flora', 'Flora'),
    ]

    ESTADO_CONSERVACION_CHOICES = [
        ('en_peligro', 'En Peligro'),
        ('invasora', 'Invasora'),
        ('comun', 'Común'),
    ]

    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=False)
    tipo_especie = models.CharField(max_length=10, choices=TIPO_ESPECIE_CHOICES, default='fauna')
    estado_conservacion = models.CharField(max_length=15, choices=ESTADO_CONSERVACION_CHOICES, default='comun')

    def __str__(self):
        return f"{self.nombre} ({'Publicado' if self.publicado else 'Pendiente'})"

class ImagenAvistamiento(models.Model):
    avistamiento = models.ForeignKey(Avistamiento, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avistamientos/", validators=[validar_extension_imagen])



def save(self, *args, **kwargs):
    super().save(*args, **kwargs)  # Guarda el objeto primero
    if self.foto:
        nombre_especie = identificar_especie(self.foto.path)
        self.nombre = nombre_especie if nombre_especie else "Especie no identificada"
        super().save(update_fields=["nombre"])  # Guarda solo el campo nombre
