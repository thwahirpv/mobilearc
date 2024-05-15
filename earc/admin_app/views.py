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
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.utils.translation import gettext as _
import json
from cart_app.models import Order
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from admin_product_app.models import Sales
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



def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
         return redirect('admin_app:admin_login')
    return render(request, 'admin_template/index.html')
       


class user_crud_view(View):
    def load_table(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        user = UserDetails.objects.all
        if request.method == 'POST':
            search_text = request.GET.get('search_text')
            user = UserDetails.objects.filter(is_active=False).filter(Q(username=search_text)|Q(email=search_text)|Q(phone_number=search_text))
            if user is None:
                user = {'error':'user not found'}
        context = {'user':user}
        return render(request, 'admin_template/page-tables.html', context)
    
    def blocked_users(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        user = UserDetails.objects.filter(is_active=False)
        if request.method == 'POST':
            search_text = request.GET.get('search_text')
            user = UserDetails.objects.filter(Q(username=search_text)|Q(email=search_text)|Q(phone_number=search_text))
        if user is None:
            user = {'error': 'user is not found'}
        context = {'user':user}
        return render(request, 'admin_template/blocked_users.html', context)

    
    def create_user(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
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
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
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
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        url = request.META.get('HTTP_REFERER')
        user = get_object_or_404(UserDetails, user_id=id)
        user.is_active = False
        user.save()
        if url:
            return redirect(url)
        else:
            return redirect('admin_app:load_table')
    
    def unblock_user(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        url = request.META.get('HTTP_REFERER')
        user = get_object_or_404(UserDetails, user_id=id)
        user.is_active = True
        user.save()
        if url:
            return redirect(url)
        else:
            return redirect('admin_app:load_table')
    
    def delete(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
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
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    return render(request, 'admin_template/settings.html')

# Logo
def logo(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
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



def sales_report(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    if request.method == 'POST':
        start = request.POST.get('start-date', None)
        end = request.POST.get('end-date', None)

        if start and end:
            sales_data = Order.objects.filter(status=4, update_at__range=[start, end])
        elif start:
            sales_data = Order.objects.filter(status=4, update_at__date=start)
        elif end:
            sales_data = Order.objects.filter(status=4, update_at__date=end)
        else:
            sales_data = Order.objects.filter(status=4).all()


        context = {
            'sales_data':sales_data
        }
        return render(request, 'admin_template/sales_report.html', context)
    


def get_chart_data(request):
    monthly_sales = Sales.objects.annotate(month=TruncMonth('sale_date')).values('month').annotate(total_sale=Count('sale_id'))
    yearly_sales = Order.objects.filter(status=4).annotate(year=TruncYear('created_at')).values('year').annotate(total_sales=Count('cart_id'))
    product_sales = Order.objects.filter(status=4).annotate(month=TruncMonth('created_at')).values('month').annotate(total_sales=Count('cart_id'))

    monthly_sales_data = [{'month': item['month'].strftime('%B'), 'total_sales':item['total_sale']} for item in monthly_sales]
    yearly_sales_data = [{'year': item['year'].year, 'total_sales': item['total_sales']} for item in yearly_sales]
    product_monthly_sales = [{'month': item['month'].strftime('%B'), 'total_sales':item['total_sales']} for item in product_sales]

    
    context = {
        'monthly_sales_data':monthly_sales_data,
        'yearly_sales_data':yearly_sales_data,
        'product_monthly_sales':product_monthly_sales
    }
    return JsonResponse(context,safe=True)
