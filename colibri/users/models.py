from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.admin.models import LogEntry
from django.core.mail import send_mail
from django.conf import settings

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

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Solo si es nueva
        super().save(*args, **kwargs)
        if is_new and self.log and self.log.user.email:
            send_mail(
                subject="Nueva Auditoría asignada",
                message=f"Se ha creado una auditoría relacionada a: {self.log.object_repr}\n\nComentario: {self.comentario}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.log.user.email],
                fail_silently=True
            )

    def __str__(self):
        return f"{self.log.object_repr} - {self.get_estado_display()}"

class MensajeAuditoria(models.Model):
    auditoria = models.ForeignKey(Auditoria, related_name='mensajes', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username}: {self.contenido[:30]}..."
