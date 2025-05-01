from datetime import datetime
from .models import EliminacionParcialAvistamiento

def eliminar_registros_expirados_avistamientos():
    ahora = datetime.now()
    EliminacionParcialAvistamiento.objects.filter(fecha_expiracion__lt=ahora).delete()