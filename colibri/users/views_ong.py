from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from reportes.models import Reporte
from avistamientos.models import Avistamiento
from .models import NotificacionONG
from django.utils import timezone
from django.db.models import Q

@login_required
def dashboard_ong(request):
    """Vista del panel principal para usuarios ONG"""
    # Verificar que el usuario pertenezca al grupo ONGs
    if not request.user.groups.filter(name='ONGs').exists():
        return redirect('inicio')
    
    # Obtener estadísticas para el dashboard
    total_reportes = Reporte.objects.count()
    reportes_sin_atender = Reporte.objects.filter(en_atencion=False).count()
    reportes_recientes = Reporte.objects.order_by('-fecha_reporte')[:5]
    
    # Asegurarnos de que filtramos correctamente y hay datos
    avistamientos_relevantes = Avistamiento.objects.filter(
        Q(estado_conservacion='en_peligro') | Q(estado_conservacion='invasora'),
        publicado=True  # Solo avistamientos publicados
    ).order_by('-fecha_creacion')[:5]
    
    # Debug: imprimir cuántos avistamientos encontramos
    print(f"Avistamientos relevantes encontrados: {avistamientos_relevantes.count()}")
    
    # Obtener notificaciones no leídas
    notificaciones = NotificacionONG.objects.filter(
        ong=request.user,
        leida=False
    )[:5]
    
    context = {
        'total_reportes': total_reportes,
        'reportes_sin_atender': reportes_sin_atender,
        'reportes_recientes': reportes_recientes,
        'avistamientos_relevantes': avistamientos_relevantes,
        'notificaciones': notificaciones
    }
    
    return render(request, 'users/ong/dashboard.html', context)

@login_required
def lista_reportes_ong(request):
    """Vista para mostrar la lista de reportes de maltrato para ONGs"""
    # Verificar que el usuario pertenezca al grupo ONGs
    if not request.user.groups.filter(name='ONGs').exists():
        return redirect('inicio')
    
    # Obtener filtros de la URL
    estado = request.GET.get('estado', None)
    tipo = request.GET.get('tipo', None)
    ubicacion = request.GET.get('ubicacion', None)
    
    # Filtrar reportes según parámetros
    # Corregir aquí también: fecha_reporte en lugar de fecha_creacion
    reportes = Reporte.objects.all().order_by('-fecha_reporte')
    
    if estado == 'sin_atender':
        reportes = reportes.filter(en_atencion=False)
    elif estado == 'en_atencion':
        reportes = reportes.filter(en_atencion=True)
    
    if tipo:
        reportes = reportes.filter(tipo_reporte=tipo)
    
    if ubicacion:
        reportes = reportes.filter(ubicacion__icontains=ubicacion)
    
    # Configurar paginación
    paginator = Paginator(reportes, 10)  # 10 reportes por página
    page = request.GET.get('page', 1)
    reportes_paginados = paginator.get_page(page)
    
    context = {
        'reportes': reportes_paginados,
        'filtro_estado': estado,
        'filtro_tipo': tipo,
        'filtro_ubicacion': ubicacion
    }
    
    return render(request, 'users/ong/lista_reportes.html', context)

@login_required
def detalle_reporte_ong(request, reporte_id):
    """Vista detalle de un reporte específico"""
    # Verificar que el usuario pertenezca al grupo ONGs
    if not request.user.groups.filter(name='ONGs').exists():
        return redirect('inicio')
    
    reporte = get_object_or_404(Reporte, id=reporte_id)
    
    # Lógica para marcar el reporte como "en atención" por esta ONG
    if request.method == 'POST' and 'aceptar_ayuda' in request.POST:
        reporte.en_atencion = True
        reporte.atendido_por = request.user
        reporte.fecha_atencion = timezone.now()
        reporte.save()
        # Podríamos añadir un mensaje de éxito aquí
    
    context = {
        'reporte': reporte
    }
    
    return render(request, 'users/ong/detalle_reporte.html', context)

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """Vista para marcar una notificación como leída"""
    # Verificar que el usuario pertenezca al grupo ONGs
    if not request.user.groups.filter(name='ONGs').exists():
        return redirect('inicio')
    
    notificacion = get_object_or_404(NotificacionONG, id=notificacion_id, ong=request.user)
    notificacion.leida = True
    notificacion.save()
    
    # Redirigir a la página anterior o al dashboard
    redirect_url = request.META.get('HTTP_REFERER', 'dashboard_ong')
    return redirect(redirect_url)