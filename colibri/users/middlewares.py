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
            
class BiologoAdminMiddleware(MiddlewareMixin):
    """Middleware para limitar la visibilidad de módulos en el admin para biólogos"""
    def process_request(self, request):
        if request.path.startswith("/admin/") and request.user.is_authenticated:
            if request.user.groups.filter(name='Biologoa').exists() and not request.user.is_superuser:
                # Permitir acceso solo a las apps avistamientos y reportes
                allowed_apps = ['/admin/', '/admin/avistamientos/', '/admin/reportes/']
                
                # Si intenta acceder a otra sección del admin, redirigir al índice del admin
                is_allowed = any(request.path.startswith(app) for app in allowed_apps)
                if not is_allowed and not request.path == '/admin/':
                    return redirect('/admin/')
