from django.http import HttpResponse
from django.shortcuts import render
from .models import Avistamiento
from .models import ImagenAvistamiento
from django.shortcuts import render, redirect
import json
from .forms import AvistamientoForm, ImagenAvistamientoForm
from django.contrib import messages

def listar_avistamientos(request):
    tipo_especie = request.GET.get('tipo_especie')
    estado_conservacion = request.GET.get('estado_conservacion')

    avistamientos = Avistamiento.objects.filter(publicado=True)

    # Aplicar filtros si están presentes
    if tipo_especie:
        avistamientos = avistamientos.filter(tipo_especie=tipo_especie)
    if estado_conservacion:
        avistamientos = avistamientos.filter(estado_conservacion=estado_conservacion)

    avistamientos_json = json.dumps([
        {
            "nombre": a.nombre,
            "descripcion": a.descripcion,
            "fecha_creacion": a.fecha_creacion.strftime("%Y-%m-%d"),
            "latitud": a.latitud,
            "longitud": a.longitud,
            "tipo_especie": a.tipo_especie,
            "estado_conservacion": a.estado_conservacion,
            "imagen_url": ImagenAvistamiento.objects.filter(avistamiento=a).first().imagen.url if ImagenAvistamiento.objects.filter(avistamiento=a).exists() else None
        }
        for a in avistamientos
    ])

    return render(request, 'avistamientos/lista.html', {
        'avistamientos': avistamientos,
        'avistamientos_json': avistamientos_json,
        'tipo_especie': tipo_especie,
        'estado_conservacion': estado_conservacion
    })

def agregar_avistamiento(request):
    if request.method == 'POST':
        form = AvistamientoForm(request.POST)
        
        if form.is_valid():
            avistamiento = form.save(commit=False)
            avistamiento.usuario = request.user  # <- Asignar el usuario actual
            avistamiento.publicado = False
            avistamiento.save()

            imagenes_validas = []
            for file in request.FILES.getlist('imagenes'):
                imagen_form = ImagenAvistamientoForm({'avistamiento': avistamiento.id}, {'imagen': file})
                if imagen_form.is_valid():  # Ahora validamos correctamente usando Django Forms
                    imagenes_validas.append(ImagenAvistamiento(avistamiento=avistamiento, imagen=file))
                else:
                    messages.error(request, f"Formato no permitido: {file.name}")

            if imagenes_validas:
                ImagenAvistamiento.objects.bulk_create(imagenes_validas)

            messages.success(request, "Tu avistamiento ha sido enviado y está pendiente de aprobación.")
            return redirect('listar_avistamientos')

    else:
        form = AvistamientoForm()
        imagenes_form = ImagenAvistamientoForm()

    return render(request, 'avistamientos/agregar.html', {'form': form, 'imagenes_form': imagenes_form})


def inicio(request):
    return render(request, 'layouts/home.html')
