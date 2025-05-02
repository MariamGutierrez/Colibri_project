from django.contrib import admin
from .models import TipoReporte, Reporte, EliminacionParcialAvistamiento
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

    def delete_model(self, request, obj):
        EliminacionParcialAvistamiento.objects.create(
            usuario=obj.usuario,  # Asegúrate de que el modelo tiene este campo
            titulo=obj.titulo,
            mensaje="Este avistamiento ha sido rechazado por no cumplir con los criterios."  # Puedes hacerlo dinámico si gustas
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            EliminacionParcialAvistamiento.objects.create(
                usuario=obj.usuario,
                titulo=obj.titulo,
                mensaje="Este avistamiento ha sido rechazado por no cumplir con los criterios."
            )
        queryset.delete()


admin.site.register(Reporte, ReporteAdmin)

@admin.register(EliminacionParcialAvistamiento)
class EliminacionParcialAvistamientoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_eliminacion', 'fecha_expiracion')
    search_fields = ('titulo',)

@admin.register(TipoReporte)
class TipoReporteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)