from django.core.mail import send_mail

def notificar_autoridades(reporte):
    asunto = f"Nuevo Reporte de Maltrato Animal - {reporte.id_reporte}"
    mensaje = f"""
    Se ha registrado un nuevo caso de maltrato animal:
    
    Descripción: {reporte.descripcion}
    Ubicación: {reporte.latitud}, {reporte.longitud}
    
    Por favor, tomar medidas necesarias.
    """
    send_mail(asunto, mensaje, 'notificaciones@plataforma.com', ['autoridades@ejemplo.com'])
