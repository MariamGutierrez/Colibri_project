from django.urls import path
from . import views

urlpatterns = [
    path('', views.seleccionar_region, name='seleccionar_region'),
    path('seleccionar-tipo-articulo/', views.seleccionar_tipo_articulo, name='seleccionar_tipo_articulo'),
    path('categoria/<str:categoria>/', views.articulos_por_categoria, name='articulos_por_categoria'),
    path('articulo/<int:id>/', views.articulo_detalle, name='articulo_detalle'),  # Nueva ruta
]