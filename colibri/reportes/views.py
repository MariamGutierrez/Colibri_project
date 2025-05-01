from django.shortcuts import render, redirect
from .models import Reporte
from .forms import ReporteForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .utils import enviar_reporte_por_correo
from django.contrib import messages

@login_required
def reportar_maltrato(request):
    if request.method == "POST":
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, "Reporte enviado correctamente.")
            return redirect("lista_reportes")
        else:
            # Personalizar mensajes de error para los archivos
            for field, errors in form.errors.items():
                if field in ['imagen', 'video', 'audio']:
                    for error in errors:
                        if 'extension' in error:
                            if field == 'imagen':
                                messages.error(request, "Error en imagen: Solo se permiten archivos JPG o PNG")
                            elif field == 'video':
                                messages.error(request, "Error en video: Solo se permiten archivos MP4 o MOV")
                            elif field == 'audio':
                                messages.error(request, "Error en audio: Solo se permiten archivos MP3 o WAV")
                        else:
                            messages.error(request, f"Error en {field}: {error}")
                else:
                    for error in errors:
                        messages.error(request, f"Error en {field}: {error}")

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
