from django.http import JsonResponse
from django.shortcuts import redirect, render
from admin_product_app.models import category, brands, products, Colors, Images, Storage
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import *
import json
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger


def list_coupens(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    page = request.GET.get('page', 1)

    try:
         coupen_data = Coupen.objects.all().order_by('-coupen_id')
    except:
         pass
    
    paginator_obj = Paginator(coupen_data, 10)
    try:
         coupen_data = paginator_obj.get_page(page)
    except PageNotAnInteger:
        coupen_data = paginator_obj.get_page(1)
    except EmptyPage:
         coupen_data = paginator_obj.get_page(paginator_obj.num_pages)
    
    context = {
         'coupen_data':coupen_data
    }

    return render(request, 'admin_template/coupen_list.html', context)



def add_coupen(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    if request.method == 'POST':
        coupen_name = request.POST.get('coupen_name', None)
        coupen_code = request.POST.get('coupen_code', None)
        coupen_percentage = request.POST.get('coupen_percentage', None)
        max_amount = request.POST.get('max_amount', None)
        expire_date = request.POST.get('expire_date', None)
        coupon_stock = request.POST.get('coupon_stock')

        
        if coupen_name is None or coupen_name == '' or coupen_name.isdigit():
            messages.warning(request, 'Enter valid name!')
        elif Coupen.objects.filter(coupen_name__icontains=coupen_name).exists():
            messages.warning(request, 'name is already exist!')
        elif coupen_code is None or coupen_code == '':
            messages.warning(request, 'Enter vaild coupen!')
        elif Coupen.objects.filter(coupen_code__icontains=coupen_code).exists():
            messages.warning(request, 'Code already exits!')
        elif coupen_percentage is None or coupen_percentage == '' or coupen_percentage.isalpha():
            messages.warning(request, 'Enter valid price!')
        elif max_amount is None or max_amount == '' or max_amount.isalpha():
            messages.warning(request, 'Enter valid Condition amount!')
        elif expire_date is None or expire_date == '':
            messages.warning(request, 'Enter valid date and time!')
        elif int(coupon_stock) < 0 or coupon_stock == '' or coupon_stock.isalpha():
            messages.warning(request, 'Enter valid stock!')

        try:
            Coupen.objects.create(
                coupen_name=coupen_name, 
                coupen_code=coupen_code, 
                coupen_percentage=coupen_percentage, 
                max_amount=max_amount, 
                expiration_date=expire_date,
                coupen_stock=coupon_stock
            )
        except Exception as e:
            messages.warning(request, e)
            return redirect('admin_coupen_app:add_coupen')
        return redirect('admin_coupen_app:list_coupens')
    return render(request, 'admin_template/add_coupen.html')


def block_and_unblock(request, id):
    try:
        coupen_obj = Coupen.objects.get(coupen_id=id)
    except:
        return redirect('admin_coupen_app:list_coupens')
    
    if coupen_obj:
        if coupen_obj.is_active:
            coupen_obj.is_active = False
            coupen_obj.save()
        else:
            coupen_obj.is_active = True
            coupen_obj.save()
        
        return redirect('admin_coupen_app:list_coupens')
    else:
        return redirect('admin_coupen_app:list_coupens')


def expire_coupen(request, id):
    try:
        coupen_obj = Coupen.objects.get(coupen_id=id)
    except:
        return redirect('admin_coupen_app:list_coupens')
    
    if coupen_obj:
        if coupen_obj.is_expire:
            coupen_obj.is_expire = False
            coupen_obj.save()
        else:
            coupen_obj.is_expire = True
            coupen_obj.save()
        return redirect('admin_coupen_app:list_coupens')
    else:
        return redirect('admin_coupen_app:list_coupens')
    
def update_coupen(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    try:
        coupen_obj = Coupen.objects.get(coupen_id=id)
    except:
        return redirect('admin_coupen_app:list_coupens')
        
    
    if request.method == 'POST':
        coupen_name = request.POST.get('coupen_name', coupen_obj.coupen_name)
        coupen_code = request.POST.get('coupen_code', coupen_obj.coupen_code)
        coupen_percentage = request.POST.get('coupen_percentage', coupen_obj.coupen_percentage)
        max_amount = request.POST.get('max_amount', coupen_obj.max_amount)
        expire_date = request.POST.get('expire_date', None)
        coupon_stock = request.POST.get('coupon_stock', coupen_obj.coupen_stock)

        
        if coupen_name is None or coupen_name == '' or coupen_name.isdigit():
            messages.warning(request, 'Enter valid name!')
        elif Coupen.objects.filter(coupen_name__icontains=coupen_name).exists():
            messages.warning(request, 'name is already exist!')
        elif coupen_code is None or coupen_code == '':
            messages.warning(request, 'Enter vaild coupen!')
        elif Coupen.objects.filter(coupen_code__icontains=coupen_code).exists():
            messages.warning(request, 'Code already exits!')
        elif coupen_percentage is None or coupen_percentage == '' or coupen_percentage.isalpha():
            messages.warning(request, 'Enter valid price!')
        elif max_amount is None or max_amount == '' or max_amount.isalpha():
            messages.warning(request, 'Enter valid Condition amount!')
        elif coupon_stock < 0 or coupon_stock == '' or coupon_stock.isalpha():
            messages.warning(request, 'Enter valid stock!')
        

        try:
            coupen_obj.coupen_name = coupen_name
            coupen_obj.coupen_code = coupen_code
            coupen_obj.coupen_percentage = coupen_percentage
            coupen_obj.max_amount = max_amount
            coupen_obj.expiration_date = expire_date if expire_date else coupen_obj.expiration_date
            coupen_obj.coupen_stock = coupon_stock
            coupen_obj.save()
        except Exception as e:
            messages.warning(request, e)
            return redirect('admin_coupen_app:add_coupen')
        return redirect('admin_coupen_app:list_coupens')
    
    context = {
        'coupen_obj':coupen_obj
    }
    return render(request, 'admin_template/add_coupen.html', context)
        


def coupen_details(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    try:
        coupen_obj = Coupen.objects.get(coupen_id=id)
    except:
        return redirect('admin_coupen_app:list_coupens') 
    
    if coupen_obj:
        context = {
            'coupen_obj':coupen_obj
        }
        return render(request, 'admin_template/coupen_details.html', context)
    else:
        return redirect('admin_coupen_app:list_coupens')



def delete_coupen(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    try:
        coupen_obj = Coupen.objects.get(coupen_id=id)
    except:
        coupen_obj = Coupen.objects.none()
    
    if coupen_obj:
        coupen_obj.delete()
        return redirect('admin_coupen_app:list_coupens')
    else:
        return redirect('admin_coupen_app:list_coupens')

          
        
     