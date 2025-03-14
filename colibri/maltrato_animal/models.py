from django.db import models
from django.forms import ValidationError
import requests
import os


from django.db import models
def validar_extension_imagen(value):
    ext = value.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('Solo se permiten imágenes en formato JPG y PNG.')

class ReporteMaltrato(models.Model):
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
    email = models.CharField(max_length=255, default='')
    telefono = models.CharField(max_length=255, default='')
    tipo_especie = models.CharField(max_length=10, choices=TIPO_ESPECIE_CHOICES, default='fauna')
    estado_conservacion = models.CharField(max_length=20, choices=ESTADO_CONSERVACION_CHOICES, default='comun')

    def __str__(self):
        return f"{self.nombre} ({'Publicado' if self.publicado else 'Pendiente'})"

 # Asegúrate de que este import esté al inicio del archivo

class Evidencia(models.Model):
    reporte = models.ForeignKey(ReporteMaltrato, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="maltrato_animal/", validators=[validar_extension_imagen], default="default.jpg")


# Create your models here.
