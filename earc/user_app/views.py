from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from admin_app.models import userdetails

# Create your views here.

# User registration
def user_registraion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conform_pass = request.POST.get('conform_pass')
        
def user_home(request):
    return render(request, 'user_template/index.html')
    