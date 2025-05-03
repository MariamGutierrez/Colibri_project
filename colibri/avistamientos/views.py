from django.http import HttpResponse
from django.shortcuts import render
from .models import Avistamiento, EliminacionParcialAvistamiento, ImagenAvistamiento
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
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para agregar un avistamiento.")
        return redirect('login')

    if request.method == 'POST':
        form = AvistamientoForm(request.POST)
        imagenes = request.FILES.getlist('imagenes')

        # Verificación de cantidad de imágenes
        if len(imagenes) > 10:
            messages.error(request, "⚠️ No puedes subir más de 10 imágenes.")
            return render(request, 'avistamientos/agregar.html', {
                'form': form,
                'imagenes_form': ImagenAvistamientoForm()
            })

        imagenes_validas = []
        errores_imagenes = False

        for file in imagenes:
            imagen_form = ImagenAvistamientoForm({'avistamiento': 0}, {'imagen': file})
            if imagen_form.is_valid():
                imagenes_validas.append(imagen_form.cleaned_data['imagen'])
            else:
                errores_imagenes = True
                messages.error(request, f"Formato no permitido: {file.name}")

        if form.is_valid() and imagenes_validas and not errores_imagenes:
            avistamiento = form.save(commit=False)
            avistamiento.usuario = request.user  # Asignar el usuario autenticado
            avistamiento.publicado = False
            avistamiento.save()

            for img in imagenes_validas:
                ImagenAvistamiento.objects.create(avistamiento=avistamiento, imagen=img)

            messages.success(request, "Tu avistamiento ha sido enviado y está pendiente de aprobación.")
            return redirect('listar_avistamientos')
        else:
            if not imagenes_validas:
                messages.error(request, "Debes subir al menos una imagen válida.")
    else:
        form = AvistamientoForm()

    return render(request, 'avistamientos/agregar.html', {
        'form': form,
        'imagenes_form': ImagenAvistamientoForm()
    })

def inicio(request):
    return render(request, 'layouts/home.html')

def eliminar_avistamiento(request, avistamiento_id):
    avistamiento = Avistamiento.objects.get(id=avistamiento_id)
    if request.method == "POST":
        EliminacionParcialAvistamiento.objects.create(titulo=avistamiento.titulo)
        messages.error(request, f"Tu avistamiento '{avistamiento.titulo}' ha sido rechazado. Esta notificación se eliminará después de 4 días hábiles.")
        avistamiento.delete()
        return redirect('listar_avistamientos')