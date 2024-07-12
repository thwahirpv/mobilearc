from django.shortcuts import render, redirect
from admin_app.models import Address
from cart_app.models import Owner, Order, Payment
from django.db.models import Q
from django.http import JsonResponse
import json
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from checkout_app.models import review
from admin_app.models import Wallet, wallet_history


def order_list(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    order_data = Order.objects.all().exclude(status=0).order_by('-cart_id')
    page = request.GET.get('page', 1)
    sort_by = None

    if request.GET:
        if request.GET.get('sort_by'):
            sort_by = int(request.GET.get('sort_by', None))
            if sort_by is not None:
                if sort_by == 1:
                    order_data = order_data.filter(status=sort_by)
                elif sort_by == 2:
                    order_data = order_data.filter(status=sort_by)
                elif sort_by == 3:
                    order_data = order_data.filter(status=sort_by)
                elif sort_by == 4:
                    order_data = order_data.filter(status=sort_by)
                elif sort_by == 5:
                    order_data = order_data.filter(status=sort_by)
                elif sort_by == 6:
                    order_data = order_data.filter(status=sort_by)
                elif sort_by == 7:
                    order_data = order_data.filter(status=sort_by)

    
    paginator_obj = Paginator(order_data, 10)
    try:
        order_data = paginator_obj.get_page(page)
    except PageNotAnInteger:
        order_data = paginator_obj.page(1)
    except EmptyPage:
        order_data = paginator_obj.page(paginator_obj.num_pages)

    context = {
        'order_data':order_data,
        'status':Order.ORDER_STATUS,
        'sort_by':sort_by
    }
    return render(request, 'admin_template/order_list.html', context)

def update_status(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        value = int(data.get('value'))

        try:
            order_obj = Order.objects.get(cart_id=id)
        except:
            context = {
                'status': False,
                'title': 'Update failed',
            }
            return JsonResponse(context, safe=True)
        
       
        
        if order_obj:
            if value == 5:
                if order_obj.is_delivered:
                     order_obj.status = 4
                     order_obj.save()
                else:
                     if order_obj.order_payment.payment_status:
                        try:
                            wallet_obj, created = Wallet.objects.get_or_create(
                                user = request.user
                            )
                        except:
                            wallet_obj = Wallet.objects.none()
                        
                        if wallet_obj:
                            wallet_obj.balance += order_obj.total_price
                            wallet_obj.save()
                            wallet_history_obj = wallet_history.objects.create(
                                wallet_owner=wallet_obj,
                                order_item=order_obj,
                                amount=order_obj.total_price,
                                status='Credit'
                            )
                            order_obj.order_payment.payment_status = False
                            order_obj.order_payment.save()
                        
                     order_obj.status = value
                     order_obj.is_delivered = False
                     order_obj.save()
                     order_obj.storage.stock = order_obj.storage.stock + order_obj.quantity
                     order_obj.storage.save()
                     order_obj.product.sold_out -= order_obj.quantity
                     order_obj.product.save()
                     order_obj.product.pro_brand.sold_out -= order_obj.quantity
                     order_obj.product.pro_brand.save()
                     order_obj.product.pro_category.sold_out -= order_obj.quantity
                     order_obj.product.pro_category.save()
            else:
                if value == 4:
                    order_obj.is_delivered = True
                    order_obj.status = value
                    order_obj.save()
                    order_obj.order_payment.payment_status = True
                    order_obj.order_payment.save()
                elif value == 7:
                    try:
                        wallet_obj, created = Wallet.objects.get_or_create(
                             user=order_obj.order_customer.customer
                        )
                    except:
                        context = {
                            'status': False,
                            'title': 'Something problem!',
                        }
                        return JsonResponse(context, safe=True)
                    
                    if wallet_obj:
                         try:
                              wallet_history_obj = wallet_history.objects.create(
                                   wallet_owner=wallet_obj,
                                   order_item=order_obj,
                                   amount=order_obj.total_price,
                                   status='Credit'
                              )
                         except:
                            context = {
                            'status': False,
                            'title': 'Something problem!',
                            }
                            return JsonResponse(context, safe=True)
                              
                         order_obj.status = value
                         order_obj.is_delivered = False
                         order_obj.save()
                         order_obj.order_payment.payment_status = False
                         order_obj.order_payment.save()
                         order_obj.product.sold_out -= order_obj.quantity
                         order_obj.product.save()
                         order_obj.product.pro_brand.sold_out -= order_obj.quantity
                         order_obj.product.pro_brand.save()
                         order_obj.product.pro_category.sold_out -= order_obj.quantity
                         order_obj.product.pro_category.save()
                         order_obj.storage.stock += order_obj.quantity
                         order_obj.storage.save()
                         wallet_obj.balance += order_obj.total_price
                         wallet_obj.save()
                    else:
                        context = {
                            'status': False,
                            'title': 'Something problem!',
                        }
                        return JsonResponse(context, safe=True)
                else:
                     order_obj.status = value
                     order_obj.is_delivered = False
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