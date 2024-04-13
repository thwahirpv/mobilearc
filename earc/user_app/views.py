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
from banner_app.models import Banner
from admin_product_app.models import products, Colors, Images
from django.db.models import Max, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
                                                                                       
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

def otp_checking(request):
    if request.user.is_authenticated:
        return redirect('user_app:user_login')
    if request.user.is_active: 
        print('is active')
        return redirect('user_app:user_login')
    

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
                messages.success(request, 'OTP verification succesfully completed', extra_tags='text-success')
                return redirect('user_app:user_login')
            else:
                messages.error(request, 'You entered wrong OTP!')
                return redirect('user_app:otp_checking')
    else:
        expiration_time = timezone.make_aware(datetime.fromtimestamp(float(request.session.get('otp_timestamp')))) + timedelta(minutes=2)
        remaining_time = max(timedelta(0), expiration_time - timezone.now())
        remaining_minutes, remaining_seconds = divmod(remaining_time.seconds, 60)
        return render(request, 'user_template/page-otp.html', {'remaining_minutes': remaining_minutes, 'remaining_seconds': remaining_seconds, 'email':request.session.get('user_email')})

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
        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_app:user_home') 
        else:
            messages.error(request, 'email or password is incorrect!', extra_tags='text-danger')        
    return render(request, 'user_template/page-login.html')

def user_logout(request):
    logout(request)
    request.session.flush()         
    return redirect('user_app:user_home')
# Home page

def user_home(request):
    context = {}
    if request.user.is_authenticated and request.user.is_active is True:
        user = request.user
        first_banner = Banner.objects.filter(Q(banner_active=True) & Q(banner_type='first_banner')).order_by('priority')
        secondary_banner = Banner.objects.filter(Q(banner_active=True) & Q(banner_type='secondary_banner'))

        latest_products = products.objects.filter(product_active=True).order_by('-product_id')[:8].prefetch_related(
            Prefetch('colors', queryset=Colors.objects.order_by('-color_id')[:1].prefetch_related(
                Prefetch('images', queryset=Images.objects.order_by('priority')[:1], to_attr='pic')
            ), to_attr='color')
        )
        context = {
            'user':user,
            'first_banner':first_banner,
            'secondary_banner':secondary_banner,
            'latest_products':latest_products
        }
    else:
        return render(request, 'user_template/index.html')

    return render(request, 'user_template/index.html', context)
    
    

def forget_password_user_conform(request):
    print('iam tochc this function')
    print(request.method)
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        print('now iam inside the post method')
        if UserDetails.objects.filter(email=email).exists():
            user_obj = UserDetails.objects.get(email=email)
            request.session['email'] = user_obj.email
            context = {
                'status': 'success',
                'user_profile':user_obj.profile.url,
            }
            return JsonResponse(context, safe=True)
        else:
            context = {
                'status': 'fail',
                'text': 'email is not exits!'
            }
            return JsonResponse(context, safe=True)
    return render(request, 'user_template/otp-email.html')


def sent_forget_password_otp(request):
    email = request.session.get('email')
    user = UserDetails.objects.get(email=email)
    signals.pre_create.send(sender=UserDetails, instance=user)
    request.session['otp_timestamp'] = str(timezone.now().timestamp())
    request.session['otp'] = user.otp
    return redirect('user_app:forget_password')



def forget_password(request):
    if request.method == 'POST':
        otp_one = request.POST.get('otp_one', None)
        otp_two = request.POST.get('otp_two', None)
        otp_three = request.POST.get('otp_three', None)
        otp_four = request.POST.get('otp_four', None)
        otp_five = request.POST.get('otp_five', None)
        otp_six = request.POST.get('otp_six', None)
        timestamp_str = request.session.get('otp_timestamp')
        email = request.session.get('email')
        user = UserDetails.objects.get(email=email)
        otp = request.session.get('otp')
        conbined_otp = otp_one + otp_two + otp_three + otp_four + otp_five + otp_six
        if conbined_otp:
            entered_otp = int(conbined_otp)

        expiration_time = timezone.make_aware(datetime.fromtimestamp(float(timestamp_str))) + timedelta(minutes=2)
        current_time = timezone.now()
        if current_time > expiration_time:
            messages.error(request, 'OTP has expired. Request new one!', extra_tags='text-danger')
            return redirect('user_app:forget_password')
        else:
            valid = otp_message_handler().check_otp(otp, entered_otp)
            if valid:
                del request.session['otp_timestamp']
                del request.session['otp']
                user.otp = None
                user.save()
                messages.success(request, 'OTP is successfully verified', extra_tags='text-success')
                return redirect('user_app:change_password')
            else:
                messages.error(request, 'Entered OTP is incorrect!')
                return redirect('user_app:forget_password')
    try:
        expiration_time = timezone.make_aware(datetime.fromtimestamp(float(request.session.get('otp_timestamp')))) + timedelta(minutes=2)
        remaining_time = max(timedelta(0), expiration_time - timezone.now())
        remaining_minutes, remaining_seconds = divmod(remaining_time.seconds, 60)
    except Exception:
        return redirect('user_app:forget_password_user_conform')
    return render(request, 'user_template/page-otp.html', {'remaining_minutes': remaining_minutes, 'remaining_seconds': remaining_seconds, 'email':request.session.get('email'), 'status':'forgot_otp'})

    

def change_password(request):
    if request.method == 'POST':
        email = request.session.get('email')
        user = get_object_or_404(UserDetails, email=email)
        password = request.POST.get('password')
        conform_password = request.POST.get('conform_password')
        print(password, conform_password)
        print(user.email)
        print('old password:', user.password)

        try:
            validate_password(password)
        except:
            messages.error(request, 'password length should have 8 \n and atleast one character and number', extra_tags='text-danger')
            return redirect('user_app:change_password')
        
        if not password == conform_password:
            messages.error(request, 'Password is not match!', extra_tags='text-danger')
            print('its not match')
            return redirect('user_app:change_password')
        
        user.set_password(password)
        user.save()
        print('after changing:', user.email, user.password)
        del request.session['email']
        messages.success(request, 'Password Successfully changed', extra_tags='text-success')
        return redirect('user_app:user_login')
    return render(request, 'user_template/change_password.html')