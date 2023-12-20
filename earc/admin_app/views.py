from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import userdetails

# Create your views here.



# Admin login 
@never_cache
def admin_login(request):
    log_error=None

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_app:admin_dashboard')
        else:
            log_error='email or password is incorrect.'

    return render(request, 'admin_template/page-account-login.html', {'log_error':log_error})


# Admin Dashboard
@login_required(login_url='login/')
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin_template/index.html')
    else:
        return redirect('admin_app:admin_login')

# Admin logout
@never_cache
def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('admin_app:admin_login')
    