from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.



# Admin login 
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_app:admin_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_app:admin_dashboard')

    return render(request, 'admin_template/page-account-login.html')


# Admin Dashboard
# @login_required(login_url='login/')
def admin_dashboard(request):
    return render(request, 'admin_template/index.html')


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
    