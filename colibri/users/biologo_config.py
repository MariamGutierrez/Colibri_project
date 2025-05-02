from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from avistamientos.models import Avistamiento, ImagenAvistamiento, EliminacionParcialAvistamiento
from reportes.models import Reporte, TipoReporte, EliminacionParcialReporte

def configurar_permisos_biologo():
    """Configura los permisos para el grupo Biologoa"""
    # Obtener o crear el grupo Biologoa
    grupo_biologo, _ = Group.objects.get_or_create(name='Biologoa')
    
    # Limpiar permisos existentes
    grupo_biologo.permissions.clear()
    
    # Modelos para los que otorgaremos permisos
    modelos_permitidos = [
        # Modelos de avistamientos
        Avistamiento, ImagenAvistamiento, EliminacionParcialAvistamiento,
        # Modelos de reportes
        Reporte, TipoReporte, EliminacionParcialReporte,
    ]
    
    # Asignar todos los permisos para cada modelo
    for modelo in modelos_permitidos:
        content_type = ContentType.objects.get_for_model(modelo)
        permisos = Permission.objects.filter(content_type=content_type)
        for permiso in permisos:
            grupo_biologo.permissions.add(permiso)
    
    return grupo_biologo