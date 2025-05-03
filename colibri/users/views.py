from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistroVisitanteForm
from django.contrib import messages
from .utils import UserDAO
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Auditoria, MensajeAuditoria  # ajusta el import si están en otra app


def registro_visitante(request):
    if request.method == 'POST':
        form = RegistroVisitanteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después de registrarse
            return redirect('inicio')  # Cambia 'home' por la vista a donde quieras redirigirlo
    else:
        form = RegistroVisitanteForm()
    
    return render(request, 'users/registro_visitante.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = UserDAO.get_user_by_email(email)

        if user and user.check_password(password):
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect("/admin/")
            else:
                return redirect("inicio")
        else:
            messages.error(request, "Credenciales Incorrectas. Intente nuevamente.")

    return render(request, "users/login.html")

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            new_password = get_random_string(length=12)
            user.set_password(new_password)
            user.save()

            html_message = render_to_string('users/email_new_password.html', {
                'username': user.username,
                'password': new_password,
            })

            send_mail(
                'Tu nueva contraseña',
                f'Tu nueva contraseña es: {new_password}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=html_message,
            )

        return redirect('forgot_password_done')

    return render(request, 'users/forgot_password_form.html')

def forgot_password_done(request):
    return render(request, 'users/forgot_password_done.html')

@login_required
def responder_auditoria(request, pk):
    auditoria = get_object_or_404(Auditoria, pk=pk)

    if request.method == "POST":
        MensajeAuditoria.objects.create(
            auditoria=auditoria,
            autor=request.user,
            contenido=request.POST.get("mensaje")
        )
        return redirect('responder_auditoria', pk=pk)

    mensajes = auditoria.mensajes.select_related('autor').order_by('timestamp')
    return render(request, 'auditorias/chat.html', {
        'auditoria': auditoria,
        'mensajes': mensajes
    })
