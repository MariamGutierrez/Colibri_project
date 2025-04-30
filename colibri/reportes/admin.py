from django.contrib import admin
from django.utils.html import format_html
from .models import TipoReporte, Reporte
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

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
    readonly_fields = ('fecha_reporte','preview_imagen', 'preview_video', 'preview_audio')
    fields = (
        'usuario', 'tipo_reporte', 'descripcion', 'ubicacion',
        'latitud', 'longitud', 'alerta_enviada',
        'imagen', 'preview_imagen',
        'video', 'preview_video',
        'audio', 'preview_audio'
    )
    actions = [enviar_alerta_por_correo]

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;" />', obj.imagen.url)
        return "No hay imagen"

    def preview_video(self, obj):
        if obj.video:
            return format_html(
                '<video width="320" height="240" controls><source src="{}" type="video/mp4">Tu navegador no soporta video.</video>',
                obj.video.url
            )
        return "No hay video"

    def preview_audio(self, obj):
        if obj.audio:
            return format_html(
                '<audio controls><source src="{}" type="audio/mpeg">Tu navegador no soporta audio.</audio>',
                obj.audio.url
            )
        return "No hay audio"

admin.site.register(Reporte, ReporteAdmin)
admin.site.register(TipoReporte)