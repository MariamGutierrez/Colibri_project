from django.db import models

class Animal(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
