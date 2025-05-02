from django.urls import path
from .views import registro_visitante, registro_ong, registro_selector, login_view, forgot_password, forgot_password_done
from .views_ong import (
    dashboard_ong, 
    lista_reportes_ong, 
    detalle_reporte_ong,
    marcar_notificacion_leida
)

urlpatterns = [
    path('registro/', registro_selector, name='registro_selector'),
    path('registro/visitante/', registro_visitante, name='registro_visitante'),
    path('registro/ong/', registro_ong, name='registro_ong'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('forgot-password/done/', forgot_password_done, name='forgot_password_done'),
    
    # Rutas específicas para ONG
    path('dashboard/ong/', dashboard_ong, name='dashboard_ong'),
    path('reportes/ong/', lista_reportes_ong, name='lista_reportes_ong'),
    path('reportes/ong/<int:reporte_id>/', detalle_reporte_ong, name='detalle_reporte_ong'),
    path('notificaciones/leer/<int:notificacion_id>/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
]