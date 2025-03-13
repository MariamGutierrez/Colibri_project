from django.http import HttpResponse
from django.shortcuts import render
from .models import Avistamiento
from .models import ImagenAvistamiento
from django.shortcuts import render, redirect
import json
from .forms import AvistamientoForm, ImagenAvistamientoForm

def listar_avistamientos(request):
    avistamientos = Avistamiento.objects.all()
    
    # Convertir avistamientos a JSON para que JavaScript pueda usarlo
    avistamientos_json = json.dumps([
        {
            "nombre": a.nombre,
            "descripcion": a.descripcion,
            "latitud": a.latitud,
            "longitud": a.longitud,
            "fotos": [img.imagen.url for img in ImagenAvistamiento.objects.filter(avistamiento=a)]
        }
        for a in avistamientos
    ])


    return render(request, 'avistamientos/lista.html', {
        'avistamientos': avistamientos,
        'avistamientos_json': avistamientos_json  # Enviamos el JSON al template
    })


def agregar_avistamiento(request):
    if request.method == 'POST':
        form = AvistamientoForm(request.POST)
        imagenes_form = ImagenAvistamientoForm(request.POST, request.FILES)
        
        if form.is_valid():
            avistamiento = form.save()
            
            for file in request.FILES.getlist('imagenes'):
                ImagenAvistamiento.objects.create(avistamiento=avistamiento, imagen=file)

            return redirect('listar_avistamientos')

    else:
        form = AvistamientoForm()
        imagenes_form = ImagenAvistamientoForm()

    return render(request, 'avistamientos/agregar.html', {'form': form, 'imagenes_form': imagenes_form})


