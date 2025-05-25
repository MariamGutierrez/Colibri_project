from django.shortcuts import render, redirect
from .models import Reporte
from .forms import ReporteForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .utils import enviar_reporte_por_correo
from django.contrib import messages
from django.contrib.messages import get_messages

@login_required
def reportar_maltrato(request):
    if request.method == "POST":
        form = ReporteForm(request.POST, request.FILES)
        
        # Validar cantidad de archivos
        imagenes = request.FILES.getlist('imagen')
        videos = request.FILES.getlist('video')
        audios = request.FILES.getlist('audio')
        
        if len(imagenes) == 0:
            form.add_error('imagen', "Debes adjuntar al menos una imagen")
        elif len(imagenes) > 10:
            form.add_error('imagen', "No puedes subir más de 10 imágenes")
        
        if len(videos) > 2:
            form.add_error('video', "No puedes subir más de 2 videos")
            
        if len(audios) > 2:
            form.add_error('audio', "No puedes subir más de 2 audios")
        
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, "Reporte enviado correctamente.")
            return redirect("lista_reportes")
    else:
        form = ReporteForm()

    return render(request, "reportes/reportar.html", {"form": form})


class ListaReportesView(ListView):
    model = Reporte
    template_name = 'reportes/lista_reportes.html'
    context_object_name = 'reportes'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reporte.objects.all().order_by('-fecha_reporte')
        else:
            return Reporte.objects.filter(usuario=self.request.user).order_by('-fecha_reporte')

@staff_member_required
def enviar_alerta(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)

    if not reporte.alerta_enviada:
        enviar_reporte_por_correo(reporte)
        reporte.alerta_enviada = True
        reporte.save()

    return redirect('lista_reportes')
