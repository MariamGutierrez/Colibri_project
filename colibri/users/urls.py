from django.urls import path
from .views import registro_visitante, login_view, forgot_password, forgot_password_done
from . import views


urlpatterns = [
    path('registro/', registro_visitante, name='registro_visitante'),
    path("login/", login_view, name="login"),
    path('auditorias/<int:pk>/chat/', views.responder_auditoria, name='responder_auditoria'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('forgot-password/done/', forgot_password_done, name='forgot_password_done'),
]
