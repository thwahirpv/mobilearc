from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from admin_app.models import userdetails
from django.contrib import messages



# User registration
def user_registraion(request):
    # redirect home page When comming already authenticated user 
    if request.user.is_authenticated:
        return redirect('user_app:user_home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        conform_pass = request.POST.get('conform_password')

        if userdetails.objects.filter(email=email).exists() or userdetails.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'email or phone nummber is already exits!')
            return redirect('user_app:user_registraion')
        else:
            if password == conform_pass:
                print("---------------")
                user = userdetails.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
                user.is_active = False
                user.save()
                user_id = request.session['user_id'] = user.user_id   
                return redirect('user_app:user_otp')
            else:
                messages.error(request, 'password is not match!')
                return redirect('user_app:user_registraion')

    return render(request, 'user_template/page-registration.html')

# otp verification
def user_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('user_id')
        del request.session['user_id']
        user = userdetails.objects.get(user_id=user_id)

        if otp == user.otp:
            user.otp = None
            user.is_active = True
            user.save()
            request.session['email'] = user.email
            return redirect('user_app:user_login')
        else:
            messages.error(request, 'Entered opt is invalid! enter correct otp.')
    
    return render(request, 'user_template/page-otp.html')

def user_login(request):
    if request.user.authenticate:
        return redirect('user_app:user_home')
    return render(request, 'page-login.html')

def user_home(request):
    if request.user.is_authenticated and request.user.is_active:
        return render(request, 'user_template/index.html')
    else:
        return redirect('user_app:user_registraion')
    