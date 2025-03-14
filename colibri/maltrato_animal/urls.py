from django.urls import path
from . import views

urlpatterns = [
    path('maltrato_animal/reportar/', views.reportar_maltrato, name='reportar_maltrato'),
    path('maltrato_animal/lista/', views.lista_reportes, name='lista_reportes'),
    path('maltrato_animal/<uuid:id_reporte>/', views.detalle_reporte, name='detalle_reporte'),
]

