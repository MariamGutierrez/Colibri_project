from django.urls import path
from .views import listar_avistamientos, agregar_avistamiento

urlpatterns = [
    path('', listar_avistamientos, name='listar_avistamientos'),
    path('agregar/', agregar_avistamiento, name='agregar_avistamiento'),
]