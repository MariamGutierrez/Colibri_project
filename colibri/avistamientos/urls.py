from django.urls import path
from .views import listar_avistamientos, agregar_avistamiento, eliminar_avistamiento

urlpatterns = [
    path('', listar_avistamientos, name='listar_avistamientos'),
    path('agregar/', agregar_avistamiento, name='agregar_avistamiento'),
    path('eliminar_avistamiento/<int:avistamiento_id>/', eliminar_avistamiento, name='eliminar_avistamiento'),
]