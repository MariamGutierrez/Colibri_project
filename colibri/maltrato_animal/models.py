from django.db import models
from django.core.validators import FileExtensionValidator
import uuid

from django.db import models
from django.core.validators import FileExtensionValidator
import uuid

class ReporteMaltrato(models.Model):
    id_reporte = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    descripcion = models.TextField(verbose_name="Descripción del caso")
    latitud = models.FloatField()
    longitud = models.FloatField()
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True, 
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    audio = models.FileField(upload_to='audios/', blank=True, null=True, 
                             validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto')
    ], default='pendiente')

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.estado}"

class Evidencia(models.Model):
    reporte = models.ForeignKey(ReporteMaltrato, related_name="evidencias", on_delete=models.CASCADE)
    archivo = models.FileField(
        upload_to="evidencias/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'mp4', 'mp3'])]
    )
    tipo = models.CharField(max_length=10, choices=[('foto', 'Foto'), ('video', 'Video'), ('audio', 'Audio')])

    def __str__(self):
        return f"Evidencia para Reporte {self.reporte.id_reporte}"


# Create your models here.
