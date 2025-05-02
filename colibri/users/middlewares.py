from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages

class AdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            if not request.user.is_authenticated or not request.user.is_staff:
                logout(request)
                return redirect('/login/')  # o la vista que uses para login general
            request.session.set_expiry(0)
            request.session.modified = True

class ONGRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Excluir explícitamente la página de registro de ONGs
        if request.path == reverse('registro_ong'):
            return None
            
        # Verificar si la URL contiene "ong"
        if 'ong' in request.path:
            # Si el usuario no está autenticado, redirigir al login
            if not request.user.is_authenticated:
                messages.error(request, "Debe iniciar sesión para acceder a esta sección.")
                return redirect('login')
            
            # Si el usuario no es una ONG, redirigir a inicio
            if not request.user.groups.filter(name='ONGs').exists():
                messages.error(request, "No tiene permisos para acceder a esta sección.")
                return redirect('inicio')
