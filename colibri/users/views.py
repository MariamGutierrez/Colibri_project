from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroVisitanteForm
from django.contrib import messages
from .utils import UserDAO

def registro_visitante(request):
    if request.method == 'POST':
        form = RegistroVisitanteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroVisitanteForm()
    
    return render(request, 'users/registro_visitante.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email").strip()  # Elimina espacios en blanco
        password = request.POST.get("password")
        
        user = None
        error_message = ""
        
        # Verificamos si es un email (contiene @)
        if '@' in username_or_email:
            user = UserDAO.get_user_by_email(username_or_email)
            if not user:
                error_message = "No existe una cuenta con este email."
        else:
            user = UserDAO.get_user_by_username(username_or_email)
            if not user:
                error_message = "No existe un usuario con este nombre."
        
        # Si encontramos al usuario pero la contraseña es incorrecta
        if user and not user.check_password(password):
            error_message = "La contraseña es incorrecta."
        
        if user and not error_message:
            login(request, user)
            return redirect("inicio")
        else:
            messages.error(request, error_message or "Credenciales inválidas.")
    
    return render(request, "users/login.html")