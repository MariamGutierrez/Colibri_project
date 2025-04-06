from django.urls import path
from . import views

urlpatterns = [
    path('reportar/', views.reportar_maltrato, name='reportar_maltrato'),
    path('lista/', views.ListaReportesView.as_view(), name='lista_reportes'),
    path('enviar_alerta/<int:reporte_id>/', views.enviar_alerta, name='enviar_alerta'),

]
