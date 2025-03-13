from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin

User = get_user_model()

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


