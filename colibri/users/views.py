from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistroVisitanteForm
from django.contrib import messages
from .utils import UserDAO
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
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = UserDAO.get_user_by_username(username)

        if user and user.check_password(password):
            login(request, user)
            return redirect("inicio")  
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "users/login.html")

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
