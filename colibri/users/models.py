from django.db import models
from django.contrib.auth.models import User

class Animal(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class PerfilONG(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_ong')
    nombre_organizacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    sitio_web = models.URLField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_fundacion = models.DateField(blank=True, null=True)
    area_enfoque = models.CharField(max_length=100, blank=True, null=True)
    verificada = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_organizacion

class NotificacionONG(models.Model):
    ong = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_ong')
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50, choices=[
        ('especie_peligro', 'Especie en Peligro'),
        ('especie_invasora', 'Especie Invasora'),
        ('reporte_maltrato', 'Reporte de Maltrato')
    ])
    url_relacionada = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_creacion']