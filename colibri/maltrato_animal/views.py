from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ReporteMaltrato, Evidencia
from .forms import ReporteMaltratoForm, EvidenciaForm

def reportar_maltrato(request):
    if request.method == 'POST':
        form = ReporteMaltratoForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Guardar el reporte de maltrato
            reporte = form.save(commit=False)
            reporte.publicado = False  # No se publica automáticamente
            reporte.save()

            # Procesar las imágenes enviadas
            for file in request.FILES.getlist('imagenes'):
                evidencia = Evidencia(reporte=reporte, imagen=file)
                evidencia.save()

            messages.success(request, "Tu reporte ha sido enviado y está pendiente de aprobación.")
            return redirect('lista_reportes')

        else:
            messages.error(request, "Hubo un error al enviar el reporte. Revisa los datos ingresados.")

    else:
        form = ReporteMaltratoForm()

    return render(request, 'maltrato_animal/reportar.html', {'form': form})


# Vista para listar reportes
def lista_reportes(request):
    reportes = ReporteMaltrato.objects.all().order_by('-fecha_creacion')
    return render(request, 'maltrato_animal/lista_reportes.html', {'reportes': reportes})

# Vista para ver detalles de un reporte específico
def detalle_reporte(request, id_reporte):
    reporte = get_object_or_404(ReporteMaltrato, id_reporte=id_reporte)
    return render(request, 'maltrato_animal/detalle_reporte.html', {'reporte': reporte})

