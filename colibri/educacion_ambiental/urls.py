from django.urls import path
from . import views

urlpatterns = [
    path('', views.educacion_ambiental_home, name='educacion_ambiental_home'),
    path('categoria/<str:categoria>/', views.articulos_por_categoria, name='articulos_por_categoria'),
    path('articulo/<int:id>/', views.articulo_detalle, name='articulo_detalle'),
]