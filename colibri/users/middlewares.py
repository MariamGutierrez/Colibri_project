from django.utils.deprecation import MiddlewareMixin

class AdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            request.session.set_expiry(0)  # Expira al cerrar navegador
            request.session.modified = True