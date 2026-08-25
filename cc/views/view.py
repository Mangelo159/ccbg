from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..forms import CambiarClaveForm


@login_required
def home(request):
    if request.method == 'POST':
        # Procesar el formulario, guardar datos, etc.
        return redirect('home')
    else:
        return render(request, 'cc/home/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'cc/login/login.html', {
                'error': 'Usuario o contraseña incorrectos.',
                'username': username,
            })
    else:
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'cc/login/login.html')


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def cambiar_clave(request):
    if request.method == 'POST':
        form = CambiarClaveForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, 'cc/cambiar_clave/cambiar_clave.html', {
                'form': CambiarClaveForm(request.user),
                'exito': True,
            })
    else:
        form = CambiarClaveForm(request.user)
    return render(request, 'cc/cambiar_clave/cambiar_clave.html', {'form': form})
