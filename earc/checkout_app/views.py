from django.shortcuts import render, redirect
from admin_app.models import Address
from cart_app.models import Owner, Order, Payment
from django.db.models import Q
from django.http import JsonResponse
from .models import review
from django.urls import reverse
import json


# Create your views here.


def checkout(request):
    if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
    
    user = request.user
    address_data = Address.objects.filter(user=user)
    owner_obj, created = Owner.objects.get_or_create(
        customer=user
    )
    order_data = Order.objects.filter(
        order_customer=owner_obj,
        status = 0
    )

    context = {
        'user':user,
        'address_data':address_data,
        'order_data':order_data
    }
    return render(request, 'user_template/shop-checkout.html', context)


def place_order(request):
    if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = data.get('payment_method', None)
        order_type = data.get('order_type', None)
        address_id = data.get('select_address', None)
        payment_id = data.get('payment_id', None)
        print(payment_method, order_type, address_id)

        try:
            owner_obj = Owner.objects.get(
                customer = request.user,
            )
        except:
            context = {
                'status': False
            }
            return JsonResponse(context, safe=True)
        
        try:
            address_obj = Address.objects.get(
                address_id=address_id
            )
        except:
            context = {
                'status': False
            }
            return JsonResponse(context, safe=True)

        if order_type == 'multiple':
            try:
                order_obj = Order.objects.filter(
                    order_customer = owner_obj,
                    status = 0
                )
                for item in order_obj:
                    payment_obj = Payment.objects.create(payment_mode=payment_method, payment_id=payment_id, payment_status = True if payment_method == 'online_payment' else False)
                    item.status = 1
                    item.order_address = address_obj
                    item.order_payment = payment_obj
                    item.save()
                    item.storage.stock = item.storage.stock - 1
                    item.storage.save() 
                context = {
                    'status': True
                }
                return JsonResponse(context, safe=True)
            except:
                context = {
                      'status':True
                }
                return JsonResponse(context, safe=True)         
        else:
            pass



def order_history(request):
    if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
    
    try:
        owner_obj = Owner.objects.get(customer=request.user)
    except Exception as e:
        Owner.objects.none()

    try:
        order_data = Order.objects.filter(order_customer=owner_obj).exclude(status=0).order_by('-cart_id')
    except Exception as e:
        order_data = Order.objects.none()


    context = {
        'order_data':order_data
    }
    return render(request, 'user_template/order_history.html', context)


    
def order_details(request, id):
    if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
    
    order_obj = Order.objects.get(cart_id=id)
    try:
        rating_obj = review.objects.filter(
            product=order_obj.product,
            customer = order_obj.order_customer.customer
        )
    except:
        rating_obj = review.objects.none()
    context = {
        'order_obj':order_obj,
        'rating_obj':rating_obj
    }
    return render(request, 'user_template/order_details.html', context)


def cancel_order(request,action, id):
    if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
    
    try:
        order_obj = Order.objects.get(cart_id=id)
    except:
        context = {
            'status': False,
            'title': 'Item not found!'
        }
        return JsonResponse(context, safe=True)

    if action == 'get_order':
        if order_obj.status == 5:
            context = {
                'status': False,
                'name': order_obj.product.product_name,
                'title': 'This order is already cancelled'
            }
            return JsonResponse(context, safe=True)
        else:
            context = {
                'status': True,
                'name': order_obj.product.product_name,
                'text': 'Are you sure to cancel this order'
            }
            return JsonResponse(context, safe=True)
    else:
        order_obj.status = 5
        order_obj.save()
        order_obj.storage.stock = order_obj.storage.stock + 1
        order_obj.storage.save()
        context = {
            'status': True,
            'name':order_obj.product.product_name,
            'text': 'Order cancelled'
        }
        return JsonResponse(context, safe=True)

                    
                    
def rate_review(request): 
    if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
     
    if request.method == 'POST':
        rating_value = request.POST.get('rate')
        comment = request.POST.get('comment')
        cart_id = request.POST.get('cart_id')
        print(rating_value, comment, cart_id)

        try:
            order_obj = Order.objects.get(cart_id=cart_id)
        except:
            context = {
                 'status': False,
                 'rating': 'its not completed'
            }
            return JsonResponse(context, safe=True)
        
        try:
            rating_obj =review.objects.create(
                 comment=comment, 
                 rate=rating_value, 
                 product = order_obj.product,
                 customer = order_obj.order_customer.customer
            )
            
            context = {
                 'status': True,
                 'rating': rating_obj.rate
            }
            return JsonResponse(context, safe=True)
        except:
            context = {
                 'status': False,
                 'rating': 'its not completed'
            }
            return JsonResponse(context, safe=True)

        
def order_placed(request):
    if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
    
    context = {
        'username':request.user.username
    }
    return render(request, 'user_template/order_conform_page.html', context)
          
