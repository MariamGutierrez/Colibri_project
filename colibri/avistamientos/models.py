from django.db import models
import requests
import os
from django.contrib.auth.models import User
from datetime import timedelta, date
# from apps.avistamientos.views import identificar_especie  # Esto causa un error de importación circular
from avistamientos.utils import identificar_especie 
from django.core.exceptions import ValidationError
from django.utils.timezone import now

def validar_extension_imagen(value):
    ext = value.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('Solo se permiten imágenes en formato JPG y PNG.')
    
class Hashtag(models.Model):
    texto = models.CharField(max_length=50, unique=True)
    es_predeterminado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"#{self.texto}"
    
# En una migración o en un fixture
hashtags_predeterminados = [
    "flora", "fauna", "enextincion", "invasora", 
    "mamifero", "ave", "reptil", "anfibio", "insecto"
]

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
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    def __str__(self):
        return f"{self.nombre} ({'Publicado' if self.publicado else 'Pendiente'})"
    
    def delete(self, *args, **kwargs):
        # Guarda un registro en EliminacionParcialAvistamiento
        EliminacionParcialAvistamiento.objects.create(
            usuario=self.usuario,  # Relaciona el usuario que creó el avistamiento
            titulo=self.nombre,  # Usa el nombre del avistamiento como título
        )
        super().delete(*args, **kwargs)

class ImagenAvistamiento(models.Model):
    avistamiento = models.ForeignKey(Avistamiento, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avistamientos/", validators=[validar_extension_imagen])



def save(self, *args, **kwargs):
    super().save(*args, **kwargs)  # Guarda el objeto primero
    if self.foto:
        nombre_especie = identificar_especie(self.foto.path)
        self.nombre = nombre_especie if nombre_especie else "Especie no identificada"
        super().save(update_fields=["nombre"])  # Guarda solo el campo nombre

class EliminacionParcialAvistamiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    titulo = models.CharField(max_length=255)  # El título será el mismo que el del avistamiento eliminado
    mensaje = models.TextField(blank=True, null=True)  # Mensaje del administrador
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