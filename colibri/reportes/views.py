from django.shortcuts import render, redirect, get_object_or_404
from .models import Reporte, EliminacionParcialAvistamiento
from .forms import ReporteForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .utils import enviar_reporte_por_correo
from avistamientos.models import Avistamiento  # Importa el modelo de avistamientos
from django.contrib import messages
from django.db import models
from avistamientos.models import Avistamiento, EliminacionParcialAvistamiento

@login_required  # Asegura que solo usuarios autenticados pueden reportar
def reportar_maltrato(request):
    if request.method == "POST":
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)  # No guardamos aún, primero asignamos el usuario
            reporte.usuario = request.user  # Asigna el usuario autenticado
            reporte.save()  # Ahora sí guardamos
            return redirect("lista_reportes")
        else:
            print("Errores en el formulario:", form.errors)

    else:
        form = ReporteForm()

    return render(request, "reportes/reportar.html", {"form": form})

class ListaReportesView(ListView):
    model = Reporte
    template_name = 'reportes/lista_reportes.html'
    context_object_name = 'reportes'

@staff_member_required
def enviar_alerta(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)

    if not reporte.alerta_enviada:
        enviar_reporte_por_correo(reporte)
        reporte.alerta_enviada = True
        reporte.save()

    return redirect('lista_reportes')

@login_required
def ver_cuenta(request):
    avistamientos = Avistamiento.objects.filter(usuario=request.user)
    avistamientos_rechazados = EliminacionParcialAvistamiento.objects.filter(usuario=request.user)

    return render(request, 'reportes/ver_cuenta.html', {
        'avistamientos': avistamientos,
        'avistamientos_rechazados': avistamientos_rechazados,
    })


@login_required
def detalle_avistamiento(request, pk):
    avistamiento = get_object_or_404(Avistamiento, pk=pk, usuario=request.user)

    # Busca si fue rechazado
    try:
        rechazo = EliminacionParcialAvistamiento.objects.get(titulo=avistamiento.nombre, usuario=request.user)
    except EliminacionParcialAvistamiento.DoesNotExist:
        rechazo = None

    return render(request, 'reportes/detalle_avistamiento.html', {
        'avistamiento': avistamiento,
        'rechazo': rechazo
    })

@login_required
def eliminar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id, usuario=request.user)
    EliminacionParcialAvistamiento.objects.create(
        usuario=request.user,
        titulo=reporte.titulo,
        mensaje="Eliminado manualmente por el usuario."  # o un formulario para personalizar
    )
    reporte.delete()
    messages.success(request, "Reporte eliminado correctamente.")
    return redirect('ver_cuenta')
