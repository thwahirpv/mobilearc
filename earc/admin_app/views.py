from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import UserDetails
from django.db.models import Q
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import web_logo
from django.contrib import messages
from PIL import Image
from io import BytesIO
# from rest_framework.decorators import api_view


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


class user_crud_view(View):
    def load_table(request):
        user = UserDetails.objects.all
        if request.method == 'POST':
            search_text = request.GET.get('search_text')
            user = UserDetails.objects.filter(is_active=False).filter(Q(username=search_text)|Q(email=search_text)|Q(phone_number=search_text))
            if user is None:
                user = {'error':'user not found'}
        context = {'user':user}
        return render(request, 'admin_template/page-tables.html', context)
    
    def blocked_users(request):
        user = UserDetails.objects.filter(is_active=False)
        if request.method == 'POST':
            search_text = request.GET.get('search_text')
            user = UserDetails.objects.filter(Q(username=search_text)|Q(email=search_text)|Q(phone_number=search_text))
        if user is None:
            user = {'error': 'user is not found'}
        context = {'user':user}
        return render(request, 'admin_template/blocked_users.html', context)

    
    def create_user(request):
        if request.method == 'POST':
            profile = request.FILES.get('profile_photo')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password')
            if UserDetails.objects.filter(Q(email=email)|Q(phone_number=phone_number)).exists():
                return redirect('admin_app:create_user')
            else:
                user = UserDetails.objects.create_user(profile=profile, username=username, email=email, phone_number=phone_number, password=password)
                user.verification_status = True
                user.save()
                return redirect('admin_app:load_table')
        return render(request, 'admin_template/page-createuser.html')

    def update_user(request, id):
        user = get_object_or_404(UserDetails, user_id=id)    
        if request.method == 'POST':
            user.profile = request.FILES.get('profile')
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.phone_number = request.POST.get('phone_number')
            user.save()                
            return redirect('admin_app:load_table')
        return render(request, 'admin_template/page-updateuser.html', {'user':user})
    
    def block_user(request, id):
        url = request.META.get('HTTP_REFERER')
        user = get_object_or_404(UserDetails, user_id=id)
        user.is_active = False
        user.save()
        if url:
            return redirect(url)
        else:
            return redirect('admin_app:load_table')
    
    def unblock_user(request, id):
        url = request.META.get('HTTP_REFERER')
        user = get_object_or_404(UserDetails, user_id=id)
        user.is_active = True
        user.save()
        if url:
            return redirect(url)
        else:
            return redirect('admin_app:load_table')
    
    def delete(request, id):
        user = get_object_or_404(UserDetails, user_id=id)
        user.delete()
        context = {'opration':'success'}
        return JsonResponse(context, safe=False)
        

        
# Admin logout
@never_cache
def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('admin_app:admin_login')
    


def get_user(request):
    id = request.GET.get('id')
    data = UserDetails.objects.get(user_id=id)
    username = data.username
    context = {'username': username}
    return JsonResponse(context, safe=True)

# settings
def site_settings(request):
    return render(request, 'admin_template/settings.html')

# Logo
def logo(request):
    if not request.user.is_superuser:
         return redirect('admin_app:admin_login')
    
    logo_image = web_logo.objects.latest('created_at')
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            try:
                file_content = image.read()
                img = Image.open(BytesIO(file_content))
                if not img.format.lower()  in ['jpg', 'jpeg', 'png']:
                    messages.error(request, 'Upload jpg, jpeg or png!')
                    return redirect('admin_app:logo')
            except:
                messages.error(request, 'invalid file!')
                return redirect('admin_app:logo')
        else:
            messages.error(request, 'Upload image!')
            return redirect('admin_app:logo')
        

        web_logo.objects.create(logo=image)
        return redirect('admin_app:logo')
    
    context = { 
        'logo_image':logo_image
    }
    return render(request, 'admin_template/logo.html', context)