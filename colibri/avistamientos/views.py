from django.http import HttpResponse
from django.shortcuts import render
from .models import Avistamiento, EliminacionParcialAvistamiento, ImagenAvistamiento, Hashtag
from django.shortcuts import render, redirect
from django.db.models import Count, Q  # Añadir Q aquí
import json
from .forms import AvistamientoForm, ImagenAvistamientoForm
from django.contrib import messages

def listar_avistamientos(request):
    tipo_especie = request.GET.get('tipo_especie')
    estado_conservacion = request.GET.get('estado_conservacion')
    hashtags_selected = request.GET.get('hashtags', '')
    
    # Convertir los hashtags seleccionados a una lista
    hashtags_selected_list = [tag.strip() for tag in hashtags_selected.split(',') if tag.strip()]

    # Consulta base
    avistamientos = Avistamiento.objects.filter(publicado=True)

    # Aplicar filtros si están presentes
    if tipo_especie:
        avistamientos = avistamientos.filter(tipo_especie=tipo_especie)
    if estado_conservacion:
        avistamientos = avistamientos.filter(estado_conservacion=estado_conservacion)
    
    # Filtrar por hashtags si hay alguno seleccionado
    if hashtags_selected_list:
        for hashtag in hashtags_selected_list:
            avistamientos = avistamientos.filter(hashtags__texto=hashtag)

    # Obtener los hashtags más populares para los filtros
    # Corregido: distinct() antes del slice
    hashtags_populares = Hashtag.objects.filter(
        Q(es_predeterminado=True) | 
        Q(avistamiento__isnull=False)
    ).annotate(
        num_usos=Count('avistamiento')
    ).order_by('-es_predeterminado', '-num_usos').distinct()[:15]

    # Preparar datos para el mapa
    avistamientos_json = json.dumps([
        {
            "nombre": a.nombre,
            "descripcion": a.descripcion,
            "fecha_creacion": a.fecha_creacion.strftime("%Y-%m-%d"),
            "latitud": a.latitud,
            "longitud": a.longitud,
            "tipo_especie": a.tipo_especie,
            "estado_conservacion": a.estado_conservacion,
            "hashtags": [h.texto for h in a.hashtags.all()],
            "imagen_url": ImagenAvistamiento.objects.filter(avistamiento=a).first().imagen.url 
                         if ImagenAvistamiento.objects.filter(avistamiento=a).exists() else None
        }
        for a in avistamientos
    ])

    return render(request, 'avistamientos/lista.html', {
        'avistamientos': avistamientos,
        'avistamientos_json': avistamientos_json,
        'tipo_especie': tipo_especie,
        'estado_conservacion': estado_conservacion,
        'hashtags_populares': hashtags_populares,
        'hashtags_selected': hashtags_selected,
        'hashtags_selected_list': hashtags_selected_list
    })

def agregar_avistamiento(request):
    if request.method == 'POST':
        form = AvistamientoForm(request.POST)
        imagenes = request.FILES.getlist('imagenes')
        
        # Procesar hashtags
        hashtags_texto = request.POST.get('hashtags', '').strip()

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
            avistamiento.usuario = request.user
            avistamiento.publicado = False
            avistamiento.save()

            # Guardar las imágenes
            for img in imagenes_validas:
                ImagenAvistamiento.objects.create(avistamiento=avistamiento, imagen=img)

            # Procesar y guardar hashtags
            if hashtags_texto:
                hashtag_list = hashtags_texto.split()
                for tag_text in hashtag_list:
                    # Limpiar el texto del hashtag (quitar # si existe)
                    clean_tag = tag_text.strip().lower().replace('#', '')
                    if clean_tag:
                        # Obtener o crear el hashtag
                        hashtag, created = Hashtag.objects.get_or_create(
                            texto=clean_tag, 
                            defaults={'es_predeterminado': False}
                        )
                        # Añadir al avistamiento
                        avistamiento.hashtags.add(hashtag)

            messages.success(request, "Tu avistamiento ha sido enviado y está pendiente de aprobación.")
            return redirect('listar_avistamientos')
        else:
            if not imagenes_validas:
                messages.error(request, "Debes subir al menos una imagen válida.")
    else:
        form = AvistamientoForm()

    # Obtener todos los hashtags predeterminados para mostrar en el formulario
    hashtags_predeterminados = Hashtag.objects.filter(es_predeterminado=True)

    return render(request, 'avistamientos/agregar.html', {
        'form': form,
        'imagenes_form': ImagenAvistamientoForm(),
        'hashtags_predeterminados': hashtags_predeterminados
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