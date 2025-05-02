from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

class PQRS(models.Model):
    TIPO_CHOICES = [
        ('peticion', 'Petición'),
        ('queja', 'Queja'),
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia'),
    ]

    ESTADO_CHOICES = [
        ('recibido', 'Recibido'),
        ('en_proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    referencia = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='recibido')
    respuesta = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.get_tipo_display()} #{self.referencia}"
