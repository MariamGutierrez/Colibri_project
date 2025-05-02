from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .models import Auditoria
from django.utils.html import format_html

User = get_user_model()
def es_admin(user):
    return user.is_staff

admin.site.login = user_passes_test(es_admin, login_url="/")(admin.site.login)
# Agregar permisos en la vista de usuario
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


    filter_horizontal = ("groups", "user_permissions")


# Registrar modelos en el admin
admin.site.unregister(User)  # Desregistrar User para sobreescribirlo
admin.site.unregister(Group)  # Desregistra el modelo
admin.site.register(Group, GroupAdmin)  # Lo vuelve a registrar
admin.site.register(User, CustomUserAdmin)
admin.site.register(Permission)


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('log', 'estado', 'usuario_log', 'fecha')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Solo al editar
            return ('mostrar_log',)
        return ()

    def get_fields(self, request, obj=None):
        base_fields = ['log', 'estado', 'comentario']
        if obj:
            base_fields.append('mostrar_log')
        return base_fields

    def usuario_log(self, obj):
        return obj.log.user if obj.log else "(sin usuario)"
    usuario_log.short_description = "Usuario"

    def mostrar_log(self, obj):
        if not obj or not obj.log:
            return "(Sin log asociado)"
        return format_html(
            "<strong>Modelo:</strong> {}<br>"
            "<strong>Objeto:</strong> {}<br>"
            "<strong>Acción:</strong> {}<br>"
            "<strong>Mensaje:</strong> {}<br>"
            "<strong>Usuario:</strong> {}<br>"
            "<strong>Fecha:</strong> {}",
            obj.log.content_type,
            obj.log.object_repr,
            obj.log.get_action_flag_display(),
            obj.log.change_message,
            obj.log.user,
            obj.log.action_time
        )
    mostrar_log.short_description = "Detalle del Log"
