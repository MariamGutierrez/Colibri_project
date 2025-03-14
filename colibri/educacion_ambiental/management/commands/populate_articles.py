from django.core.management.base import BaseCommand
from educacion_ambiental.models import Articulo

class Command(BaseCommand):
    help = "Genera 5 artículos por cada categoría en educacion_ambiental.models.Articulo"

    def handle(self, *args, **options):
        categorias = [
            'flora',
            'fauna',
            'especies_en_peligro',
            'conservacion',
            'practicas_sostenibles',
        ]
        for categoria in categorias:
            for i in range(1, 6):  # Generar 5 artículos
                Articulo.objects.create(
                    titulo=f"Artículo {i} de {categoria}",
                    contenido="Contenido de ejemplo para el artículo.",
                    categoria=categoria,
                    publish=True
                )
            self.stdout.write(self.style.SUCCESS(
                f"Se generaron 5 artículos en la categoría: {categoria}"
            ))