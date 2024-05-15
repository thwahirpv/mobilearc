from django.db.models import Q
from user_app.signals import pre_create
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from admin_app.models import UserDetails, Address
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
from admin_product_app.models import products, Colors, Images, brands, category
from django.db.models import Max, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from admin_app.models import Wallet, wallet_history
                                                                                       
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
    first_banner = Banner.objects.filter(Q(banner_active=True) & Q(banner_type='first_banner')).order_by('priority')
    secondary_banner = Banner.objects.filter(Q(banner_active=True) & Q(banner_type='secondary_banner'))

    latest_products = products.objects.filter(product_active=True).order_by('-product_id')[:8].prefetch_related(
        Prefetch('colors', queryset=Colors.objects.order_by('-color_id')[:1].prefetch_related(
        Prefetch('images', queryset=Images.objects.order_by('priority')[:1], to_attr='pic')
        ), to_attr='color')
    )
    category_data = category.objects.filter(category_active=True)
    brands_data = brands.objects.filter(brand_active=True).order_by('-sold_out')
    best_selling_prodects = products.objects.filter(product_active=True).order_by('-sold_out')
    

    context = {
        'first_banner':first_banner,
        'secondary_banner':secondary_banner,
        'latest_products':latest_products,
        'brands_data':brands_data,
        'category_data':category_data,
        'best_selling_prodects':best_selling_prodects
        }
    if request.user.is_authenticated and request.user.is_active is True:
        user = request.user
        context['user'] = user
        return render(request, 'user_template/index.html', context)
    else:
        return render(request, 'user_template/index.html', context)
    
    

def forget_password_user_conform(request):
    if request.method == 'POST':
        email = request.POST.get('email')
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
        del request.session['email']
        user = get_object_or_404(UserDetails, email=email)
        password = request.POST.get('password')
        conform_password = request.POST.get('conform_password')
      

        try:
            validate_password(password)
        except:
            messages.error(request, 'password length should have 8 \n and atleast one character and number', extra_tags='text-danger')
            return redirect('user_app:change_password')
        
        if not password == conform_password:
            messages.error(request, 'Password is not match!', extra_tags='text-danger')
            print('its not match')
            return redirect('user_app:change_password')
        if user.is_authenticated:
            print('he is authenticated')
            user.set_password(password)
            user.save()
            user = authenticate(request, email=email, password=password)
            login(request, user)
            messages.success(request, 'Password Successfully changed', extra_tags='text-success')
            return redirect('user_app:account_view')
        else:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Successfully changed', extra_tags='text-success')
    return render(request, 'user_template/change_password.html')


def account_view(request):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    
    user = request.user
    address_data = Address.objects.filter(user=user)
    context = {
        'user':user,
        'address_data':address_data
    }
    return render(request, 'user_template/page-account.html', context)


def update_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if UserDetails.objects.filter(email=email).exists():
            user_obj = UserDetails.objects.get(email=email)
            request.session['email'] = user_obj.email
            context = {
                'email': user_obj.email,
                'user_profile':user_obj.profile.url,
            }
            return render(request, 'user_template/find_user.html', context)
        else:
            context = {
                'status': 'fail',
                'text': 'email is not exits!'
            }
            return render(request, 'user_template/find_user.html', context)
    return render(request, 'user_template/find_user.html')



def update_details(request, id):
    try:
        if request.method == 'POST':
            user_obj = get_object_or_404(UserDetails, user_id=id)
            profile = request.FILES.get('profile', user_obj.profile)
            username = request.POST.get('username', user_obj.username)
            email = request.POST.get('email', user_obj.email)
            phone_number = request.POST.get('mobile', user_obj.phone_number)

            if user_obj:
                user_obj.profile = profile
                user_obj.username = username
                user_obj.email = email
                user_obj.phone_number = phone_number
                user_obj.save()
            return redirect('user_app:account_view')
    except:
        return redirect('user_app:account_view')
    

def add_address(request):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    user = request.user
    
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            address_type = request.POST.get('address_type', None)
            building_name = request.POST.get('building_name')
            country_code = request.POST.get('country_code')
            phone = request.POST.get('phone')
            state = request.POST.get('state')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')

            next_url = request.GET.get('next')

         
            if name == '' or name.isdigit():
                messages.error(request, 'Enter valid name!')
                return redirect('user_app:add_address')
            elif address_type is None:
                messages.error('select one of them home or office!')
                return redirect('user_app:add_address')
            elif building_name == '':
                messages.error(request, 'Enter valid Building name!')
                return redirect('user_app:add_address')
            elif state == '' or state.isdigit():
                messages.error(request, 'Enter valid State!')
                return redirect('user_app:add_address')
            elif city == '' or city.isdigit():
                messages.error(request, 'Enter valid City!')
                return redirect('user_app:add_address')
            elif pincode == '' or any(pin.isalpha() for pin in pincode):
                messages.error(request, 'Enter valid pincode!')
                return redirect('user_app:add_address')
            elif address == '' or address.isdigit():
                messages.error(request, 'Enter valid Adress!')
                return redirect('user_app:add_address')
            
            
            try:
                phone_number = PhoneNumber.from_string(phone, region=country_code)
                if not phone_number.is_valid():
                    messages.error(request, 'Enter valid Number!')
                    return redirect('user_app:add_address')
            except:
                messages.error(request, 'Its not look like phone Number!')
                return redirect('user_app:add_address')

            Address.objects.create(
                name=name, 
                address_type=address_type, 
                building_name=building_name,
                phone=phone_number,
                state=state,
                city=city,
                pincode=pincode,
                address=address,
                user = user
            )
            return redirect(next_url)
    except Exception as e:
        return redirect('user_app:add_address')
    
    COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]
    context = {
        'COUNTRY_CHOICES':COUNTRY_CHOICES,
    }
    return render(request, 'user_template/add_address.html',context)



def update_address(request, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    user = request.user
    address_obj = Address.objects.get(address_id=id)
    
    try:
        if request.method == 'POST':
            name = request.POST.get('name', address_obj.name)
            address_type = request.POST.get('address_type', address_obj.address_type)
            building_name = request.POST.get('building_name', address_obj.building_name)
            country_code = request.POST.get('country_code')
            phone = request.POST.get('phone', address_obj.phone)
            state = request.POST.get('state', address_obj.state)
            city = request.POST.get('city', address_obj.city)
            pincode = request.POST.get('pincode', address_obj.pincode)
            address = request.POST.get('address', address_obj.address)

            print(name, address_type, building_name, country_code, phone, state,city, pincode, address)

            if name == '' or name.isdigit():
                messages.error(request, 'Enter valid name!')
                return redirect('user_app:add_address')
            elif address_type is None:
                messages.error('select one of them home or office!')
                return redirect('user_app:add_address')
            elif building_name == '':
                messages.error(request, 'Enter valid Building name!')
                return redirect('user_app:add_address')
            elif state == '' or state.isdigit():
                messages.error(request, 'Enter valid State!')
                return redirect('user_app:add_address')
            elif city == '' or city.isdigit():
                messages.error(request, 'Enter valid City!')
                return redirect('user_app:add_address')
            elif pincode == '' or any(pin.isalpha() for pin in pincode):
                messages.error(request, 'Enter valid pincode!')
                return redirect('user_app:add_address')
            elif address == '' or address.isdigit():
                messages.error(request, 'Enter valid Adress!')
                return redirect('user_app:add_address')
            
            
            try:
                phone_number = PhoneNumber.from_string(phone, region=country_code)
                if not phone_number.is_valid():
                    messages.error(request, 'Enter valid Number!')
                    return redirect('user_app:add_address')
            except:
                messages.error(request, 'Its not look like phone Number!')
                return redirect('user_app:add_address')


            address_obj.name = name
            address_obj.address_type = address_type
            address_obj.building_name = building_name
            address_obj.phone = phone_number
            address_obj.state = state
            address_obj.city = city
            address_obj.pincode = pincode
            address_obj.address = address
            address_obj.save()
            
            return redirect('user_app:account_view')
    except Exception as e:
        return redirect('user_app:add_address')
    
    COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]
    context = {
        'COUNTRY_CHOICES':COUNTRY_CHOICES,
        'address_obj':address_obj
    }
    return render(request, 'user_template/add_address.html',context)




def delete_address(request, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    try:
        address_obj = Address.objects.get(address_id=id)
        if address_obj:
            address_obj.delete()
            context ={
                'status':True,
                'text':'Address Deleted'
            }
            return JsonResponse(context, safe=True)
        else:
            context = {
                'status':False, 
                'text':'Address not found!'
            }
            return JsonResponse(context, safe=True)
    except Exception as e:
        context = {
            'status':False, 
            'text':'Address not found!'
        }
        return JsonResponse(context, safe=True)
    


def wallet_view(request):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    
    try:
        wallet_obj = Wallet.objects.get(user=request.user.user_id)
    except:
        wallet_obj = Wallet.objects.none()

    try:
        wallet_history_obj = wallet_history.objects.filter(wallet_owner=wallet_obj).order_by('-history_id')
    except:
        wallet_history_obj = wallet_history.objects.none()

    context = {
        'wallet_obj':wallet_obj,
        'wallet_history_obj':wallet_history_obj
    }

    return render(request, 'user_template/wallet.html', context)