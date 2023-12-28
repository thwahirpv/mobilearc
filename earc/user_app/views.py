from django.db.models import Q
from user_app.signals import pre_create
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from admin_app.models import UserDetails
from django.contrib import messages
from .signals import otp_message_handler
from django.contrib.auth.decorators import login_required                                                                                                       
from django.views.decorators.cache import never_cache                                                                                                      



# User registration
@never_cache
def user_registraion(request): 
    # already authendicated user redirect home.
    if request.user.is_authenticated and request.user.is_active: 
        return redirect('user_app:user_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        conform_pass = request.POST.get('conform_password')

        if any(field == '' for field in [username, email, phone_number, password, conform_pass]):
            messages.error(request, 'All fields are require. fill all fields!')
            return redirect('user_app:user_registraion')
        if UserDetails.objects.filter(Q(email=email)|Q(phone_number=phone_number)).exists():
            user = UserDetails.objects.get(Q(email=email)|Q(phone_number=phone_number))
            if user.verification_status is False:
                if password == conform_pass:
                    user.delete()
                    user = UserDetails.objects.create_user(email=email, phone_number=phone_number, password=password, username=username)
                    request.session['user_email'] = user.email # insert the user to session  
                    request.session['otp_timestamp'] = str(timezone.now().timestamp()) # save the timestamp to the session
                    return redirect('user_app:otp_checking')
            else:
                messages.error(request, 'email or phone nummber is already exits!')
                return redirect('user_app:user_registraion')
        else:
            if password == conform_pass:
                user = UserDetails.objects.create_user(email=email, phone_number=phone_number, password=password, username=username)
                user.save()
                request.session['user_email'] = user.email # insert the user to session  
                request.session['otp_timestamp'] = str(timezone.now().timestamp()) # save the timestamp to the session
                return redirect('user_app:otp_checking')
            else:
                messages.error(request, 'password is not match!')
                return redirect('user_app:user_registraion')
    return render(request, 'user_template/page-registration.html')


# otp verification
@never_cache
def otp_checking(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('user_email')
        timestamp_str = request.session.get('otp_timestamp')
        user = UserDetails.objects.get(email=email)

        # check otp is expire or not
        expiration_time = timezone.make_aware(datetime.fromtimestamp(float(timestamp_str))) + timedelta(minutes=2)
        current_time = timezone.now()
        if current_time > expiration_time:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return redirect('user_app:otp_checking')
        else:
            valid = otp_message_handler().check_otp(user.otp,entered_otp)
            print('this is valid:',valid)
            if valid:
                user.verification_status = True
                user.otp = None
                user.save()
                del request.session['otp_timestamp']
                del request.session['user_email']
                return redirect('user_app:user_login')
            else:
                messages.error(request, 'Entered OTP is incorrect..')
                redirect('user_app:otp_checking')
    expiration_time = timezone.make_aware(datetime.fromtimestamp(float(request.session.get('otp_timestamp')))) + timedelta(minutes=2)
    remaining_time = max(timedelta(0), expiration_time - timezone.now())
    remaining_minutes, remaining_seconds = divmod(remaining_time.seconds, 60)
    return render(request, 'user_template/page-otp.html',{'remaining_minutes': remaining_minutes, 'remaining_seconds': remaining_seconds})

# login 
@never_cache
def user_login(request):
    # already authenticated user redirect home page. 
    if request.user.is_authenticated and request.user.is_active:
        return redirect('user_app:user_home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_app:user_home')         
    return render(request, 'user_template/page-login.html')

# Home page
@login_required(login_url='user_app:user_login')
def user_home(request):
    
    return render(request, 'user_template/index.html')
    