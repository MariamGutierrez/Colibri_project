from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.utils.timezone import now

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

    titulo = models.CharField(max_length=255, default=tipo_reporte)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        # Guarda un registro en EliminacionParcialReporte
        EliminacionParcialReporte.objects.create(
            titulo=self.titulo,
        )
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Reporte {self.id} - {self.tipo_reporte.nombre}"

class EliminacionParcialReporte(models.Model):
    titulo = models.CharField(max_length=255, default="Título por defecto")
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Calcula la fecha de expiración sumando 4 días hábiles
        dias_habiles = 0
        fecha_actual = now().date()
        while dias_habiles < 4:
            fecha_actual += timedelta(days=1)
            if fecha_actual.weekday() < 5:  # Lunes a Viernes son días hábiles
                dias_habiles += 1
        self.fecha_expiracion = fecha_actual
        super().save(*args, **kwargs)

    def dias_restantes(self):
        # Calcula los días restantes dinámicamente
        hoy = date.today()
        dias_restantes = (self.fecha_expiracion.date() - hoy).days
        return max(dias_restantes, 0)