from django.urls import path
from .views import registro_visitante, login_view
from . import views


urlpatterns = [
    path('registro/', registro_visitante, name='registro_visitante'),
    path("login/", login_view, name="login"),
    path('auditorias/<int:pk>/chat/', views.responder_auditoria, name='responder_auditoria'),
]
