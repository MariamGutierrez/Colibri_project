from datetime import datetime
from .models import EliminacionParcialReporte

def eliminar_registros_expirados_reportes():
    ahora = datetime.now()
    EliminacionParcialReporte.objects.filter(fecha_expiracion__lt=ahora).delete()