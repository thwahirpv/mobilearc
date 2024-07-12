from django.shortcuts import render, redirect
from sympy import Sum
from admin_app.models import Address
from cart_app.models import Owner, Order, Payment
from django.db.models import Q
from django.http import JsonResponse
from .models import review
from django.urls import reverse
import json
from admin_coupen_app.models import Coupen
from django.contrib import messages
from datetime import datetime
import pytz
from admin_coupen_app.models import User_coupon
from .templatetags.order_tags import final_total_price
from admin_app.models import Wallet, wallet_history
import razorpay
from earc.settings import RAZORPAY_KEY_ID, RAZORPAY_SECRET_KEY
from cart_app.models import Sales
from .templatetags.order_tags import product_sub_total  




def checkout(request):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')

    
    total = 0
    coupon_applied = False
    user = request.user
    address_data = Address.objects.filter(user=user)
    owner_obj, created = Owner.objects.get_or_create(
        customer=user
    )
    order_data = Order.objects.filter(
        order_customer=owner_obj,
        status=0
    )

    for item in order_data:
        if item.storage.stock == 0:
            item.quantity = item.storage.stock
            item.save()
            messages.warning(request, f'{item.product.product_name} stock is not available try after stock came!')
            return redirect('cart_app:view_cart')
        elif item.storage.stock < item.quantity:
            item.quantity = item.storage.stock
            item.save()
            if item.storage.stock == 0:
                item.quantity = item.storage.stock
                item.save()
                messages.warning(request, f'{item.product.product_name} stock is not available try after stock came!')
                return redirect('cart_app:view_cart')
            messages.warning(request, f'{item.product.product_name} only {item.storage.stock} stock!')
            return redirect('cart_app:view_cart')
    try:
        coupons_data = Coupen.objects.exclude(used_users=user)
    except:
        coupen_data = Coupen.objects.none()

    for item in order_data:
        if item.offer_object is not None:
            discount_price = (item.product.price + int(item.storage.price_of_size)) * item.offer_object.discount_percentage / 100
            product_price = (item.product.price + int(item.storage.price_of_size)) - discount_price
            total += product_price * item.quantity
        else:
            product_price = (item.product.price + int(item.storage.price_of_size)) - item.product.discount_price
            total += product_price * item.quantity

    if request.method == 'POST':
        coupen_code = request.POST.get('coupen_code')
        coupen_obj = None
        try:
            coupen_obj = Coupen.objects.get(coupen_code=coupen_code)
        except Exception as e:
            messages.warning(request, 'Unvalid coupen')
            return redirect('checkout_app:checkout')

        if coupen_obj:
            if coupen_obj.is_active is False:
                messages.warning(request, 'Unvalid coupon',
                                 extra_tags='warning')
            elif coupen_obj.is_expire is True:
                messages.warning(request, 'Coupon expired',
                                 extra_tags='warning')
            elif coupen_obj.expiration_date < datetime.utcnow().replace(tzinfo=pytz.utc):
                messages.warning(request, 'Coupon expired', extra_tags='warning')
            elif coupen_obj.used_users.filter(user_id=request.user.user_id).exists():
                messages.warning(request, 'Already used', extra_tags='warning')
            elif coupen_obj.coupen_stock < 1:
                messages.warning(request, 'No more left', extra_tags='warning')
            elif total <= coupen_obj.max_amount:
                messages.warning(
                    request, f'Purchase above ${coupen_obj.max_amount}')
            else:
                coupen_obj.used_users.add(request.user)
                coupen_obj.coupen_stock = coupen_obj.coupen_stock - 1
                coupen_obj.save()
                owner_obj.coupon_percentage = coupen_obj.coupen_percentage
                owner_obj.coupon_code = coupen_obj.coupen_code
                owner_obj.save()
                messages.success(request, 'Applied', extra_tags='success')
                return redirect('checkout_app:checkout')

        else:
            messages.warning(request, 'coupen not exists')
    
    if owner_obj:
        if owner_obj.coupon_code:
            coupon_applied = True
        else:
            coupon_applied = False
    else:
        False


    context = {
        'user': user,
        'address_data': address_data,
        'order_data': order_data,
        'owner_obj': owner_obj,
        'total': total,
        'coupons_data':coupons_data,
        'coupon_applied': coupon_applied
    }
    return render(request, 'user_template/shop-checkout.html', context)


def razorpay_order(request):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    
    try:
        owner_obj = Owner.objects.get(
            customer=request.user,
        )
    except Exception as e:
        context = {
            'status': False,
            'text':e
        }
        return JsonResponse(context, safe=True)
    
    try:
        order_obj = Order.objects.filter(
            order_customer=owner_obj,
            status=0
        )
        total = final_total_price(order_obj, owner_obj=None)
    except Exception as e:
        context = {
            'status': False,
            'text':e
        }
        return JsonResponse(context, safe=True)
    
    for item in order_obj:
        if item.storage.stock == 0:
            item.quantity = item.storage.stock
            item.save()
            context = {
                'status':False,
                'text':f'{item.product.product_name} currently no stock!'
            }
            return JsonResponse(context, safe=True)
        elif item.storage.stock < item.quantity:
            item.quantity = item.storage.stock
            item.save()
            if item.storage.stock == 0:
                item.quantity = item.storage.stock
                item.save()
                context = {
                    'status':False,
                    'text':f'{item.product.product_name} currently no stock!'
                }
                return JsonResponse(context, safe=True)
            context = {
                'status':False,
                'text':f'{item.product.product_name} only {item.storage.stock} stock!. You can order {item.storage.stock}'
            }
            return JsonResponse(context, safe=True)
    
    
    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET_KEY))
    except Exception as e:
        context = {
            'status': False,
            'text':'Connection problem. Ensure your connection!'
        }
        return JsonResponse(context, safe=True)
    
    try:
        data = { "amount": int(total), "currency": "INR", "payment_capture":1 }
        payment = client.order.create(data=data)
        order_id = payment['id']
        context = {
            'status':True,
            'amount': data['amount'],
            'key':RAZORPAY_KEY_ID,
            'order_id':order_id,
            'currency':data['currency']
        }
        return JsonResponse(context, safe=True)
    except Exception as e:
        context = {
            'status': False,
            'text':'connection problem. Ensure your connection!'
        }
        return JsonResponse(context, safe=True)
    
    
def place_order(request):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')

    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = data.get('payment_method', None)
        order_type = data.get('order_type', None)
        address_id = data.get('select_address', None)
        payment_id = data.get('payment_id', None)

        try:
            owner_obj = Owner.objects.get(
                customer=request.user,
            )
        except Exception as e:
            context = {
                'status': False,
                'text':e
            }
            return JsonResponse(context, safe=True)
        
        try:
            order_obj = Order.objects.filter(
                    order_customer=owner_obj,
                    status=0
                )
        except Exception as e:
            context = {
                'status': False,
                'text':e
            }
            return JsonResponse(context, safe=True)
        
        for item in order_obj:
            if item.storage.stock == 0:
                item.quantity = item.storage.stock
                item.save()
                messages.warning(request, f'{item.product.product_name} stock is not available try after stock came!')
                return redirect('cart_app:view_cart')
            elif item.storage.stock < item.quantity:
                item.quantity = item.storage.stock
                item.save()
                if item.storage.stock == 0:
                    item.quantity = item.storage.stock
                    item.save()
                    messages.warning(request, f'{item.product.product_name} stock is not available try after stock came!')
                    return redirect('cart_app:view_cart')
                messages.warning(f'{item.product.product_name} only {item.storage.stock} stock!')
        try:
            address_obj = Address.objects.get(
                address_id=address_id
            )
        except Exception as e:
            context = {
                'status': False,
                'text':'Select the address'
            }
            return JsonResponse(context, safe=True)

        if payment_method == 'wallet':
            try:
                wallet_obj = Wallet.objects.get(user=request.user)
            except Exception as e:
                context = {
                    'status': False,
                    'text':"Your wallet doesn't have enough money"
                }
                return JsonResponse(context, safe=True)

        if order_type == 'multiple':
            try:
                total = final_total_price(order_obj, owner_obj=None)
                if payment_method == 'wallet':
                    if wallet_obj:
                        if wallet_obj.balance >= total:
                            wallet_obj.balance -= total
                            wallet_obj.save()
                        else:
                            context = {
                                'status': False,
                                'text': 'insufficient balance'
                            }
                            return JsonResponse(context, safe=True)
                    else:
                        context = {
                            'status': False,
                            'text': "Your wallet doesn't have enough money"
                        }
                        return JsonResponse(context, safe=True)
                elif payment_method == 'cod':
                    if total > 50000:
                        context = {
                            'status': False,
                            'text': "COD is only under 50000."
                        }
                        return JsonResponse(context, safe=True)


                for item in order_obj:
                    payment_obj = Payment.objects.create(
                        payment_mode=payment_method,
                        payment_id=payment_id,
                        payment_status=True if payment_method == 'online_payment' or 'wallet' else False
                    )
                    item.status = 1
                    item.order_address = address_obj
                    item.order_payment = payment_obj
                    item.coupon_amount = ((owner_obj.coupon_percentage/100 * total) / order_obj.count()) if owner_obj.coupon_percentage else 0
                    item.total_price = product_sub_total(item) - ((owner_obj.coupon_percentage/100 * total) / order_obj.count()) if owner_obj.coupon_percentage else product_sub_total(item)
                    item.delivery_charge = 20 
                    item.save() 
                    item.product.sold_out += item.quantity
                    item.product.save()
                    item.product.pro_brand.sold_out += item.quantity
                    item.product.pro_brand.save()
                    item.product.pro_category.sold_out += item.quantity
                    item.product.pro_category.save()
                    item.storage.stock = item.storage.stock - item.quantity
                    item.storage.save()
                
                    if payment_method == 'wallet':
                        wallet_history.objects.create(
                                wallet_owner=wallet_obj,
                                order_item=item,
                                amount=item.total_price,
                                status='Debit'
                            )
                    
                owner_obj.coupon_code = None
                owner_obj.coupon_percentage = None
                owner_obj.save()
                context = {
                    'status': True,
                    'text':"Order sucesss"
                }
                return JsonResponse(context, safe=True)
            except Exception as e:
                context = {
                    'status': False,
                    'text':e
                }
                return JsonResponse(context, safe=True)
        else:
            print('its not multipp')


def order_history(request):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')

    try:
        owner_obj = Owner.objects.get(customer=request.user)
    except Exception as e:
        Owner.objects.none()

    try:
        order_data = Order.objects.filter(
            order_customer=owner_obj).exclude(status=0).order_by('-cart_id')
    except Exception as e:
        order_data = Order.objects.none()

    context = {
        'order_data': order_data
    }
    return render(request, 'user_template/order_history.html', context)


def order_details(request, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')

    order_obj = Order.objects.get(cart_id=id)
    try:
        rating_obj = review.objects.filter(
            product=order_obj.product,
            customer=order_obj.order_customer.customer
        )
    except:
        rating_obj = review.objects.none()
    context = {
        'order_obj': order_obj,
        'rating_obj': rating_obj
    }
    return render(request, 'user_template/order_details.html', context)


def cancel_order(request, action, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')

    try:
        order_obj = Order.objects.get(cart_id=id)
    except:
        context = {
            'status': False,
            'text': 'Item not found!'
        }
        return JsonResponse(context, safe=True)

    if action == 'get_order':
        if order_obj.status == 5:
            context = {
                'status': False,
                'name': order_obj.product.product_name,
                'text': 'This order is already cancelled'
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
        if order_obj.is_delivered:
            order_obj.status = 4
            order_obj.save()
        else:
            if order_obj.order_payment.payment_status:
                try:
                    wallet_obj, created = Wallet.objects.get_or_create(
                        user=request.user
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

            order_obj.status = 5
            order_obj.is_delivered = False
            order_obj.save()
            order_obj.product.sold_out -= order_obj.quantity
            order_obj.product.save()
            order_obj.product.pro_brand.sold_out -= order_obj.quantity
            order_obj.product.pro_brand.save()
            order_obj.product.pro_category.sold_out -= order_obj.quantity
            order_obj.product.pro_category.save()
            order_obj.storage.stock = order_obj.storage.stock + order_obj.quantity
            order_obj.storage.save()
            sale_item = Sales.objects.filter(saled_product=order_obj.product)
            sale_item[0].delete()

        context = {
            'status': True,
            'name': order_obj.product.product_name,
            'text': 'Order cancelled'
        }
        return JsonResponse(context, safe=True)


def return_and_refund(request, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')

    try:
        wallet_Obj, created = Wallet.objects.get_or_create(
            user=request.user
        )
        order_obj = Order.objects.get(cart_id=id)
    except:
        context = {
            'status': False,
            'title': 'Return failed',
            'text': 'Item not found'
        }
        return JsonResponse(context, safe=True)

    if wallet_Obj and order_obj:
        try:
            wallet_history_obj = wallet_history.objects.create(
                wallet_owner=wallet_Obj,
                order_item=order_obj,
                amount=order_obj.total_price,
                status='Credit'
            )
        except:
            context = {
                'status': False,
                'title': 'Return failed',
                'text': 'Try sometime later!'
            }
            return JsonResponse(context, safe=True)
        order_obj.status = 7
        order_obj.is_delivered = False
        order_obj.save()
        order_obj.order_payment.payment_status = False
        order_obj.order_payment.save()
        order_obj.storage.stock += order_obj.quantity
        order_obj.storage.save()
        order_obj.product.sold_out -= order_obj.quantity
        order_obj.product.save()
        order_obj.product.pro_brand.sold_out -= order_obj.quantity
        order_obj.product.pro_brand.save()
        order_obj.product.pro_category.sold_out -= order_obj.quantity
        order_obj.product.pro_category.save()
        
        wallet_Obj.balance += order_obj.total_price
        wallet_Obj.save()
        context = {
            'status': True,
            'title': 'Order Returned',
            'text': f'{order_obj.total_price} credited your wallet.',
            'name': order_obj.product.product_name
        }
        return JsonResponse(context, safe=True)
    else:
        context = {
            'status': False,
            'title': 'Return failed',
            'text': 'Try to sometime later',
            'name': order_obj.product.product_name
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
            rating_obj = review.objects.create(
                comment=comment,
                rate=rating_value,
                product=order_obj.product,
                customer=order_obj.order_customer.customer
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
        'username': request.user.username
    }
    return render(request, 'user_template/order_conform_page.html', context)


def remove_coupon(request):
    try:
        owner_obj = Owner.objects.get(customer=request.user)
    except:
        owner_obj = Owner.objects.none()

    if owner_obj:
        try:
            coupon_obj = Coupen.objects.get(coupen_code=owner_obj.coupon_code)
            coupon_obj.used_users.remove(request.user)
        except:
            return redirect('checkout_app:checkout')

        owner_obj.coupon_code = None
        owner_obj.coupon_percentage = None
        owner_obj.save()
        return redirect('checkout_app:checkout')
    else:
        return redirect('checkout_app:checkout')


def order_replacement(request, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    
    try:
        order_obj = Order.objects.get(cart_id=id)
    except:
        order_obj = Order.objects.none()

    if order_obj:
        order_obj.status = 6
        order_obj.save()
        return redirect('checkout_app:order_placed')
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def invoice_details(request, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    
    try:
        order_obj = Order.objects.get(cart_id=id)
    except:
        return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'order_obj':order_obj
    }

    return render(request, 'user_template/invoice.html', context)
