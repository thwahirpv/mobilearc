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
from phonenumber_field.phonenumber import PhoneNumber
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password 
from PIL import Image
from io import BytesIO   
import pycountry
from . import signals
                                                                                       
@never_cache
def fournoterror(request):
    return render(request, 'user_template/page-404.html')

# User registration
@never_cache
def user_registration(request):
    # already authendicated user redirect home.
    if request.user.is_authenticated and request.user.is_active: 
        return redirect('user_app:user_home')
    

    if request.method == 'POST':
        profile = request.FILES.get('profile')
        username = request.POST.get('username')
        email = request.POST.get('email')
        country_code = request.POST.get('preferred_country')
        number = request.POST.get('phone')
        password = request.POST.get('password')
        conform_pass = request.POST.get('conform_password')

        # Checking proile photo valid 
        if profile:
            file_content = profile.read()
            try:
                image = Image.open(BytesIO(file_content))
                if not image.format.lower() in ['jpeg', 'jpg', 'png']:
                    messages.error(request, 'invalid image formate!. upload jpeg or png')
                    return redirect('user_app:user_registration')
            except:
                messages.error(request, 'Invalid file!')
                return redirect('user_app:user_registration')
        else:
            messages.error(request, 'upload profile!')
            return redirect('user_app:user_registration')
        
        # Checking username valid
        if len(username) < 3:
            messages.error(request, 'username minimum 3 characters!')
            return redirect('user_app:user_registration')
        if not any(letter.isalpha() for letter in username):
            messages.error(request, 'username should be include character')
            return redirect('user_app:user_registration')

        # Checking email vaild
        try:
            validate_email(email)
        except:
            messages.error(request, 'invalid Email!')
            return redirect('user_app:user_registration')
                    
        # Checking phone number valid
        try:
            phone_number = PhoneNumber.from_string(number, region=country_code)
            print(phone_number.as_international)
            if not phone_number.is_valid():
                messages.error(request, 'Invalid mobile number')
                return redirect('user_app:user_registration')
        except:
            messages.error(request, 'Did not seem to be a phone number!.')
            return redirect('user_app:user_registration')
        
        # Checking password valid
        try:
            validate_password(password)
        except:
            messages.error(request, 'password length should have 8 \n and atleast one character and number')
            return redirect('user_app:user_registration')
        


        if UserDetails.objects.filter(Q(email=email) or Q(phone_number=phone_number)).exists():
            user = UserDetails.objects.get(Q(email=email) or  Q(phone_number=phone_number))
            if user.verification_status is False:
                if password == conform_pass:
                    user.delete()
                    user = UserDetails.objects.create_user(profile=profile, email=email, phone_number=phone_number, password=password, username=username)
                    request.session['user_email'] = user.email # insert the user to session  
                    request.session['otp_timestamp'] = str(timezone.now().timestamp()) # save the timestamp to the session
                    request.session['otp'] = user.otp
                    return redirect('user_app:otp_checking')
            else:
                messages.error(request, 'email or phone nummber is already exits!')
                return redirect('user_app:user_registration')
        else:
            if password == conform_pass:
                user = UserDetails.objects.create_user(profile=profile, email=email, phone_number=phone_number, password=password, username=username)
                user.save()
                request.session['user_email'] = user.email # insert the user to session  
                request.session['otp_timestamp'] = str(timezone.now().timestamp()) # save the timestamp to the session
                request.session['otp'] = user.otp
                return redirect('user_app:otp_checking')
            else:
                messages.error(request, 'password is not match!')
                return redirect('user_app:user_registration')
    COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]
    return render(request, 'user_template/page-registration.html', {'COUNTRY_CHOICES':COUNTRY_CHOICES})


# otp verification
@never_cache
def otp_checking(request):
    if request.method == 'POST':
        otp_one = request.POST.get('otp_one')
        otp_two = request.POST.get('otp_two')
        otp_three = request.POST.get('otp_three')
        otp_four = request.POST.get('otp_four')
        otp_five = request.POST.get('otp_five')
        otp_six = request.POST.get('otp_six')
        email = request.session.get('user_email')
        timestamp_str = request.session.get('otp_timestamp')
        user = UserDetails.objects.get(email=email)
        otp = request.session.get('otp')

        conbined_otp = otp_one + otp_two + otp_three + otp_four + otp_five + otp_six
        entered_otp = int(conbined_otp)
        print(entered_otp)

        # check otp is expire or not
        expiration_time = timezone.make_aware(datetime.fromtimestamp(float(timestamp_str))) + timedelta(minutes=2)
        current_time = timezone.now()
        if current_time > expiration_time:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return redirect('user_app:otp_checking')
        else:
            valid = otp_message_handler().check_otp(otp, entered_otp)
            if valid:
                user.verification_status = True
                user.otp = None
                user.save()
                del request.session['otp_timestamp']
                del request.session['user_email']
                return redirect('user_app:user_login')
            else:
                messages.error(request, 'Entered OTP is incorrect...')
                redirect('user_app:otp_checking')
    expiration_time = timezone.make_aware(datetime.fromtimestamp(float(request.session.get('otp_timestamp')))) + timedelta(minutes=2)
    remaining_time = max(timedelta(0), expiration_time - timezone.now())
    remaining_minutes, remaining_seconds = divmod(remaining_time.seconds, 60)
    return render(request, 'user_template/page-otp.html',{'remaining_minutes': remaining_minutes, 'remaining_seconds': remaining_seconds, 'email':request.session.get('user_email')})

# resent otp
def otp_resent(request):
    email = request.GET.get('email')
    user = UserDetails.objects.get(email=email)
    signals.pre_create.send(sender=UserDetails, instance=user)
    request.session['otp_timestamp'] = str(timezone.now().timestamp())
    request.session['otp'] = user.otp
    return redirect('user_app:otp_checking')


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
        else:
            messages.error(request, 'email or password is incorrect!')        
    return render(request, 'user_template/page-login.html')

def user_logout(request):
    logout(request)
    request.session.flush()         
    return redirect('user_app:user_home')
# Home page

def user_home(request):
    user = request.user
    if request.user.is_authenticated and request.user.is_active:
        return render(request, 'user_template/index.html', {'user':user})
    else:
        return render(request, 'user_template/index.html', {'user':user})
    