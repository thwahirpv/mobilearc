import datetime as time
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from admin_app.models import userdetails
from django.contrib import messages
from .signals import otp_message_handler



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
                user = userdetails.objects.create_user(email=email,  password=password, username=username, phone_number=phone_number)
                user.is_active = False
                user.save()
                user_id = request.session['user_id'] = user.user_id  
                #save the timestamp to the session
                request.session['otp_timestamp'] = str(timezone.now().timestamp())
                return redirect('user_app:user_otp')
            else:
                messages.error(request, 'password is not match!')
                return redirect('user_app:user_registraion')

    return render(request, 'user_template/page-registration.html')

# otp verification
def user_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        user_id = request.session.get('user_id')
        del request.session['user_id']
        timestamp_str = request.session.get('otp_timestamp')
        user = userdetails.objects.get(user_id=user_id)

        # sent the otp to api 
        otp_obj = otp_message_handler(user.phone_number)
        # this function retunr otp is correct or not 
        verified = otp_obj.check_otp(otp_code)

        # Check if OTP is expired
        expiration_time = timezone.make_aware(datetime.fromisoformat(timestamp_str)) + timedelta(minutes=2)
        current_time = timezone.now()
        # check otp expire time 
        if current_time > expiration_time:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return render(request, 'userhome/otp.html')
        
        # check otp valid or not
        if verified:
            user.is_active = True
            user.save()
            return redirect('user_app:user_login')
        else:
            messages.error(request, 'Entered opt is invalid! enter correct otp.')
            return redirect('user_app:user_otp')

    expiration_time = timezone.make_aware(datetime.fromtimestamp(float(request.session.get('otp_timestamp')))) + timedelta(minutes=1)
    remaining_time = max(timedelta(0), expiration_time - timezone.now())
    remaining_minutes, remaining_seconds = divmod(remaining_time.seconds, 60)
    return render(request, 'user_template/page-otp.html',{'remaining_minutes': remaining_minutes, 'remaining_seconds': remaining_seconds})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_app:user_home')
    return render(request, 'user_template/page-login.html')

def user_home(request):
    if request.user.is_authenticated and request.user.is_active:
        return render(request, 'user_template/index.html')
    else:
        return redirect('user_app:user_registraion')
    