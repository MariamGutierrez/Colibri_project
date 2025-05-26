from django.urls import path
from .views import registro_visitante, login_view, terminos_y_condiciones

urlpatterns = [
    path('registro/', registro_visitante, name='registro_visitante'),
    path("login/", login_view, name="login"),
    path('terminos/', terminos_y_condiciones, name='terminos'),
]