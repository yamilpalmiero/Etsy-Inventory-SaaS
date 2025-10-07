from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm


def register_view(request):
    """
    Vista de registro de nuevo usuario.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada exitosamente para {username}!')
            login(request, user)  # Login automático después del registro
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Vista de inicio de sesión.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {username}!')
                # Redirigir a 'next' si existe, sino al dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Vista de cierre de sesión.
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Dashboard principal del usuario.
    Muestra resumen de tiendas y productos.
    """
    user = request.user
    stores = user.stores.all()
    
    context = {
        'user': user,
        'stores': stores,
        'total_stores': stores.count(),
    }
    
    return render(request, 'accounts/dashboard.html', context)