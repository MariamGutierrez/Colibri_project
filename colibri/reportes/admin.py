from django.contrib import admin
from .models import TipoReporte, Reporte
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages  # Reemplaza con los modelos que has creado

@admin.action(description="Enviar alerta por correo a partir del reporte")
def enviar_alerta_por_correo(modeladmin, request, queryset):
    enviados = 0
    for reporte in queryset:
        if not reporte.alerta_enviada:
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
            destinatarios = ['vakogay710@bariswc.com']

            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                destinatarios,
                fail_silently=False
            )

            reporte.alerta_enviada = True
            reporte.save()
            enviados += 1
    messages.success(request, f"{enviados} alerta(s) enviadas correctamente.")

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo_reporte', 'fecha_reporte', 'alerta_enviada')
    list_filter = ('tipo_reporte', 'alerta_enviada')
    actions = [enviar_alerta_por_correo]

admin.site.register(Reporte, ReporteAdmin)
admin.site.register(TipoReporte)