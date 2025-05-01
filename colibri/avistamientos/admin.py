from django.contrib import admin
from .models import Avistamiento, ImagenAvistamiento, EliminacionParcialAvistamiento
from django.utils.html import format_html
from django import forms

class AvistamientoAdminForm(forms.ModelForm):
    mensaje = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motivo del rechazo'}),
        label="Mensaje del Administrador"
    )

    class Meta:
        model = Avistamiento
        fields = '__all__'

@admin.register(Avistamiento)
class AvistamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'usuario', 'fecha_creacion', 'publicado')
    form = AvistamientoAdminForm

    def delete_model(self, request, obj):
        mensaje = request.POST.get('mensaje', 'Sin motivo especificado')
        EliminacionParcialAvistamiento.objects.create(
            usuario=obj.usuario,
            titulo=obj.nombre,
            mensaje=mensaje,
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        mensaje = request.POST.get('mensaje', 'Sin motivo especificado')
        for obj in queryset:
            EliminacionParcialAvistamiento.objects.create(
                usuario=obj.usuario,
                titulo=obj.nombre,
                mensaje=mensaje,
            )
        queryset.delete()

class ImagenAvistamientoAdmin(admin.ModelAdmin):
    list_display = ('avistamiento', 'preview')  # Agregar la vista previa

    def preview(self, obj):
        if obj.imagen:  # Verifica si hay imagen
            return format_html('<img src="{}" width="100" height="100" style="border-radius:10px;"/>', obj.imagen.url)
        return "(No image)"

    preview.allow_tags = True
    preview.short_description = "Vista previa"

admin.site.register(ImagenAvistamiento, ImagenAvistamientoAdmin)

@admin.register(EliminacionParcialAvistamiento)
class EliminacionParcialReporteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_eliminacion', 'fecha_expiracion')
    search_fields = ('titulo',)