from django.db import models

class Articulo(models.Model):
    CATEGORIAS = [
        ('flora', 'Flora'),
        ('fauna', 'Fauna'),
        ('especies_en_peligro', 'Especies en Peligro'),
        ('conservacion', 'Conservación'),
        ('practicas_sostenibles', 'Prácticas Sostenibles'),
    ]

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)
    imagen_principal = models.ForeignKey('ImagenArticulo', null=True, blank=True, on_delete=models.SET_NULL, related_name='articulo_principal')

    def __str__(self):
        return self.titulo

class ImagenArticulo(models.Model):
    articulo = models.ForeignKey(Articulo, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='articulos/imagenes/')

    def __str__(self):
        return f"Imagen de {self.articulo.titulo}"

class VideoArticulo(models.Model):
    articulo = models.ForeignKey(Articulo, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='articulos/videos/')

    def __str__(self):
        return f"Video de {self.articulo.titulo}"