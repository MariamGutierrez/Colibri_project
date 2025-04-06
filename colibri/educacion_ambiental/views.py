from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Articulo

def educacion_ambiental_home(request):
    return render(request, 'educacion_ambiental/seleccionar_tipo_articulo.html')

def articulo_detalle(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    return render(request, 'educacion_ambiental/articulo_detalle.html', {'articulo': articulo})

def seleccionar_region(request):
    regiones = [
        {'slug': 'andina', 'nombre': 'Región Andina'},
        {'slug': 'caribe', 'nombre': 'Región Caribe'},
        {'slug': 'pacifica', 'nombre': 'Región Pacífica'},
        {'slug': 'orinoquia', 'nombre': 'Región Orinoquía'},
        {'slug': 'amazonia', 'nombre': 'Región Amazonía'},
        {'slug': 'insular', 'nombre': 'Región Insular'},
    ]
    if request.method == 'POST':
        region = request.POST.get('region')
        if region:
            # Guardar la región en la sesión si está disponible
            if request.session:
                request.session['region_seleccionada'] = region
            # Guardar la región en una cookie si no hay sesión
            response = redirect('seleccionar_tipo_articulo')
            response.set_cookie('region_seleccionada', region, max_age=3600)  # Cookie válida por 1 hora
            return response
    return render(request, 'educacion_ambiental/seleccionar_region.html', {'regiones': regiones})

def seleccionar_tipo_articulo(request):
    # Obtener la región desde la sesión o la cookie
    region = request.session.get('region_seleccionada') or request.COOKIES.get('region_seleccionada')
    return render(request, 'educacion_ambiental/seleccionar_tipo_articulo.html', {'region': region})

def articulos_por_categoria(request, categoria=None):
    # Obtener la región desde la sesión o la cookie
    region = request.session.get('region_seleccionada') or request.COOKIES.get('region_seleccionada')
    articulos = Articulo.objects.filter(publish=True)
    if categoria:
        articulos = articulos.filter(categoria=categoria)
    if region:
        articulos = articulos.filter(region=region)
    return render(request, 'educacion_ambiental/articulos_por_categoria.html', {
        'articulos': articulos,
        'categoria': categoria,
        'region': region,
    })