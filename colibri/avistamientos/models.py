from django.db import models
import requests
import os
# from apps.avistamientos.views import identificar_especie  # Esto causa un error de importación circular
from avistamientos.utils import identificar_especie  # Ahora importamos desde utils.py


from django.db import models

class Avistamiento(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class ImagenAvistamiento(models.Model):
    avistamiento = models.ForeignKey(Avistamiento, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avistamientos/")



def save(self, *args, **kwargs):
    super().save(*args, **kwargs)  # Guarda el objeto primero
    if self.foto:
        nombre_especie = identificar_especie(self.foto.path)
        self.nombre = nombre_especie if nombre_especie else "Especie no identificada"
        super().save(update_fields=["nombre"])  # Guarda solo el campo nombre
