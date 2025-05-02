from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()
Animal = apps.get_model('users', 'Animal')  # Obtener el modelo dinámicamente
#content_type = ContentType.objects.get_for_model(Animal)

# Crear grupos
admin_group, _ = Group.objects.get_or_create(name='Administradores')
editor_group, _ = Group.objects.get_or_create(name='Editores')
viewer_group, _ = Group.objects.get_or_create(name='Visitantes')
ong_group, _ = Group.objects.get_or_create(name='ONGs')
biologist_group, _ = Group.objects.get_or_create(name='Biologoa')
# Definir permisos
permissions = [
    ('add_animal', 'Puede agregar animales'),
    ('change_animal', 'Puede modificar animales'),
    ('delete_animal', 'Puede eliminar animales'),
    ('view_animal', 'Puede ver animales'),
]

for codename, name in permissions:
    perm, _ = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        #content_type=content_type
    )
    if codename.startswith("add") or codename.startswith("change") or codename.startswith("delete"):
        admin_group.permissions.add(perm)
        editor_group.permissions.add(perm)
    else:
        viewer_group.permissions.add(perm)

