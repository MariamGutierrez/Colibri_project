from django.db import models
from django.contrib.auth.models import User

class TipoReporte(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Reporte(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_reporte = models.ForeignKey(TipoReporte, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    alerta_enviada = models.BooleanField(default=False)

    imagen = models.ImageField(upload_to='reportes/imagenes/', blank=True, null=True)
    video = models.FileField(upload_to='reportes/videos/', blank=True, null=True)
    audio = models.FileField(upload_to='reportes/audios/', blank=True, null=True)
    latitud = models.CharField(max_length=50, blank=True, null=True)
    longitud = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"Reporte {self.id} - {self.tipo_reporte.nombre}"

