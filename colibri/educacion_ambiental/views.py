from django.shortcuts import render, get_object_or_404
from .models import Articulo

def educacion_ambiental_home(request):
    return render(request, 'educacion_ambiental/home.html')

def articulos_por_categoria(request, categoria):
    articulos = Articulo.objects.filter(categoria=categoria, publish=True)  # Filtrar por artículos publicados
    return render(request, 'educacion_ambiental/articulos_por_categoria.html', {'articulos': articulos, 'categoria': categoria})

def articulo_detalle(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    return render(request, 'educacion_ambiental/articulo_detalle.html', {'articulo': articulo})