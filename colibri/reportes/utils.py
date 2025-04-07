# utils.py

from django.core.mail import send_mail
from django.conf import settings

def enviar_reporte_por_correo(reporte):
    asunto = f"Nuevo reporte: {reporte.tipo_reporte.nombre}"
    mensaje = f"""
    Usuario: {reporte.usuario.username}
    Tipo de reporte: {reporte.tipo_reporte.nombre}
    Descripción: {reporte.descripcion}
    Ubicación: {reporte.ubicacion}
    Latitud: {reporte.latitud}
    Longitud: {reporte.longitud}
    Fecha: {reporte.fecha_reporte}
    """
    destinatarios = ['laxidi4704@exclussi.com']  # puedes usar una lista de admins

    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        destinatarios,
        fail_silently=False
    )
