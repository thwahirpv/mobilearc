from django.shortcuts import render, redirect
from admin_app.models import Address
from cart_app.models import Owner, Order, Payment
from django.db.models import Q
from django.http import JsonResponse
import json
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from checkout_app.models import review


def order_list(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    order_data = Order.objects.all().exclude(status=0).order_by('-cart_id')
    page = request.GET.get('page', 1)
    print(page)

    
    paginator_obj = Paginator(order_data, 10)
    try:
        order_data = paginator_obj.get_page(page)
    except PageNotAnInteger:
        order_data = paginator_obj.page(1)
    except EmptyPage:
        order_data = paginator_obj.page(paginator_obj.num_pages)

    context = {
        'order_data':order_data,
        'status':Order.ORDER_STATUS
    }
    return render(request, 'admin_template/order_list.html', context)

def update_status(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        value = data.get('value')

        try:
            order_obj = Order.objects.get(cart_id=id)
        except:
            context = {
                'status': False,
                'title': 'Update failed',
            }
            return JsonResponse(context, safe=True)

        if order_obj:
            order_obj.status = value
            order_obj.save()
            context = {
                'status': True,
                'title': 'Successfully updated',
            }
            return JsonResponse(context, safe=True)
        else:
            context = {
                'status': False,
                'title': 'Update failed',
            }
            return JsonResponse(context, safe=True)

def order_details(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    try:
        order_obj = Order.objects.get(cart_id=id)
    except:
        order_obj = Order.objects.none()

    try:
        review_data = review.objects.filter(
            product = order_obj.product,
            customer = order_obj.order_customer.customer
        )
    except:
         review_data = review.objects.none()

    context = {
        'order_obj':order_obj,
        'status':Order.ORDER_STATUS,
        'review_data':review_data
    }

    return render(request, 'admin_template/order_details.html', context)



        
    