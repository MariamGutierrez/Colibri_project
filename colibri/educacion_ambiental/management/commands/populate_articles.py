from django.core.management.base import BaseCommand
from educacion_ambiental.models import Articulo

class Command(BaseCommand):
    help = "Genera 5 artículos por cada categoría y región en educacion_ambiental.models.Articulo"

    def handle(self, *args, **options):
        categorias = [
            'flora',
            'fauna',
            'especies_en_peligro',
            'conservacion',
            'practicas_sostenibles',
        ]
        regiones = [
            'andina',
            'caribe',
            'pacifica',
            'orinoquia',
            'amazonia',
            'insular',
        ]

        for categoria in categorias:
            for region in regiones:
                for i in range(1, 6):  # Generar 5 artículos por región
                    Articulo.objects.create(
                        titulo=f"Artículo {i} de {categoria} en {region}",
                        contenido="Contenido de ejemplo para el artículo.",
                        categoria=categoria,
                        region=region,
                        publish=True
                    )
                self.stdout.write(self.style.SUCCESS(
                    f"Se generaron 5 artículos en la categoría: {categoria}, región: {region}"
                ))