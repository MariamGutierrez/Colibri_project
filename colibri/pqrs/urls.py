from django.urls import path
from .views import enviar_pqrs, mis_pqrs

urlpatterns = [
    path('nuevo/', enviar_pqrs, name='enviar_pqrs'),
    path('mios/', mis_pqrs, name='mis_pqrs'),
]

