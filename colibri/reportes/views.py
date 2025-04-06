from django.shortcuts import render, redirect
from .models import Reporte
from .forms import ReporteForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .utils import enviar_reporte_por_correo

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
