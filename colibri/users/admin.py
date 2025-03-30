from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

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


