from django.shortcuts import render, get_object_or_404, redirect
from .models import ReporteMaltrato
from .forms import ReporteMaltratoForm

# Vista para crear un nuevo reporte
def reportar_maltrato(request):
    if request.method == 'POST':
        form = ReporteMaltratoForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save()
            return redirect('detalle_reporte', id_reporte=reporte.id_reporte)
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

