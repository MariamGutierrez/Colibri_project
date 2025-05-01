from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('reportar/', views.reportar_maltrato, name='reportar_maltrato'),
    path('lista/', views.ListaReportesView.as_view(), name='lista_reportes'),
    path('enviar_alerta/<int:reporte_id>/', views.enviar_alerta, name='enviar_alerta'),
    path('ver_cuenta/', views.ver_cuenta, name='ver_cuenta'),
    path('eliminar_reporte/<int:reporte_id>/', views.eliminar_reporte, name='eliminar_reporte'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)