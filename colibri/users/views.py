from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistroVisitanteForm
from django.contrib import messages

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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("inicio")  # Redirige a la página principal después de iniciar sesión
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "users/login.html")