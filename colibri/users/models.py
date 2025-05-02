from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.admin.models import LogEntry

class Animal(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Auditoria(models.Model):
    log = models.OneToOneField(LogEntry, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('revision', 'En revisión'),
            ('proceso', 'Proceso realizado'),
            ('resuelto', 'Resuelto'),
        ],
        default='revision'
    )
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.log.object_repr} - {self.get_estado_display()}"