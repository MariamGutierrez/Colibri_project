from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib.auth import logout

class AdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            if not request.user.is_authenticated or not request.user.is_staff:
                logout(request)
                return redirect('/login/')  # o la vista que uses para login general
            request.session.set_expiry(0)
            request.session.modified = True
