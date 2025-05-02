from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PQRSForm
from .models import PQRS
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PQRS

@login_required
def enviar_pqrs(request):
    if request.method == 'POST':
        form = PQRSForm(request.POST)
        if form.is_valid():
            pqrs = form.save(commit=False)
            pqrs.usuario = request.user
            pqrs.save()

            # Notificación al usuario
            send_mail(
                subject='📬 Hemos recibido tu solicitud PQRS',
                message=f'Tu {pqrs.get_tipo_display()} fue recibida con número de referencia: {pqrs.referencia}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )

            return render(request, 'pqrs/confirmacion.html', {'pqrs': pqrs})
    else:
        form = PQRSForm()

    return render(request, 'pqrs/formulario.html', {'form': form})

@login_required
def mis_pqrs(request):
    pqrs = PQRS.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'pqrs/mis_pqrs.html', {'pqrs': pqrs})

from django.contrib import messages

@login_required
def enviar_pqrs(request):
    if request.method == 'POST':
        form = PQRSForm(request.POST)
        if form.is_valid():
            pqrs = form.save(commit=False)
            pqrs.usuario = request.user
            pqrs.save()

            # Mensaje de confirmación con referencia
            messages.success(request, f'Tu {pqrs.get_tipo_display()} fue registrada. Referencia: {pqrs.referencia}')

            return redirect('mis_pqrs')
    else:
        form = PQRSForm()

    return render(request, 'pqrs/formulario.html', {'form': form})
