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
from .templatetags.cart_tags import sub_total
from offer_app.models import category_offer, brand_offer


class cart_management:
    def view_cart(request):
        if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
        

        owner_obj, created = Owner.objects.get_or_create(customer=request.user)
        owner_obj.coupon = None
        owner_obj.save()
        
        
        if owner_obj:
            cart_items = Order.objects.filter(order_customer = owner_obj, status=0)   
        else:
            cart_items = Order.objects.none()


        context = {
            'owner_obj':owner_obj,
            'cart_items':cart_items
        }
        return render(request, 'user_template/cart.html', context)

    def add_cart(request):
        if not request.user.is_authenticated or request.user.is_active is False: 
            context = {
                'status': 'login'
            }
            return JsonResponse(context, safe=True)
        
        if request.method == 'POST':
            color_id = request.POST.get('color_id')
            storage_id = request.POST.get('storage_id')
            quantity = int(request.POST.get('quantity'))
            offer_id = request.POST.get('offer_id')
            offer_type = request.POST.get('offer_type')
            
            color_obj = Colors.objects.get(color_id=color_id)
            product_obj = color_obj.product
            storage_obj = Storage.objects.get(size_id=storage_id)

            try:
                owner_obj, created = Owner.objects.get_or_create(
                    customer = request.user,
                )

                cart_obj, cart_created = Order.objects.get_or_create(
                    order_customer = owner_obj,
                    product = product_obj,
                    color = color_obj, 
                    storage = storage_obj,
                    status = 0
                )
                if offer_type == 'category':
                    offer_obj = category_offer.objects.get(offer_id=offer_id)
                    cart_obj.content_type = ContentType.objects.get_for_model(category_offer)
                    cart_obj.object_id = offer_obj.offer_id
                    cart_obj.save()
                elif offer_type == 'brand':
                    offer_obj = brand_offer.objects.get(offer_id=offer_id)
                    cart_obj.content_type = ContentType.objects.get_for_model(brand_offer)
                    cart_obj.object_id = offer_obj.offer_id
                    cart_obj.save()
                else:
                    offer_obj = None

                if cart_created:
                    if cart_obj.storage.stock < quantity:
                        cart_obj.quantity = cart_obj.storage.stock
                        cart_obj.save()
                    else:
                        cart_obj.quantity = quantity
                        cart_obj.save()

                else:
                    if cart_obj.storage.stock < (cart_obj.quantity + quantity):
                        cart_obj.quantity = cart_obj.storage.stock
                        cart_obj.save()
                    else:
                        cart_obj.quantity = cart_obj.quantity + quantity
                        cart_obj.save()

                context = {
                    'status':True,
                }
                return JsonResponse(context, safe=True)
            except Exception as e:
                context = {
                    'status':False
                }
                return JsonResponse(context, safe=True) 


    # remove item from cart
    def remove_item(request, id):
        if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')

        try:
            cart_obj = Order.objects.get(cart_id=id)
            if cart_obj:
                cart_obj.delete()
                context = {
                    'status':True,
                    'text':'Successfully removed'
                }
                return JsonResponse(context, safe=True)

            else:
                context = {
                    'status':False,
                    'text':'Product not found'
                }
                return JsonResponse(context, safe=True)
        except:
            context = {
                    'status':False,
                    'text':'Try sometime later'
                }   
            return JsonResponse(context, safe=True)             
            


    def update_quantity(request):
        if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
        
        if request.method == 'POST':
            data = json.loads(request.body)
            qty = data.get('qty')
            id = data.get('cart_id')
            total = 0
            try:
                cart_obj = get_object_or_404(Order, cart_id=id)
                if cart_obj:
                    if cart_obj.storage.stock < qty:
                        context = {
                            'status': 'stockout',
                            'text':'Out of stock',
                            'stock': cart_obj.storage.stock
                        }
                        return JsonResponse(context, safe=True)
                    else:
                        cart_obj.quantity = qty
                        cart_obj.save()
                        if cart_obj.offer_object is not None:
                            discount_price = (cart_obj.product.price + int(cart_obj.storage.price_of_size)) * cart_obj.offer_object.discount_percentage / 100
                            product_price = (cart_obj.product.price + int(cart_obj.storage.price_of_size)) - discount_price
                            total = product_price * cart_obj.quantity
                            cart_obj.total_price = total
                            cart_obj.save()
                        else:
                            product_price = (cart_obj.product.price + int(cart_obj.storage.price_of_size)) - cart_obj.product.discount_price
                            total = product_price * cart_obj.quantity
                            cart_obj.total_price = total
                            cart_obj.save()
                        
                        context = {
                            'status':True,
                            'stock': cart_obj.storage.stock,
                            'total': round(total)
                        }
                        return JsonResponse(context, safe=True)
                else:
                    context = {
                        'status':False,
                        'text':'Item not found'
                    }
                    return JsonResponse(context, safe=True)
            except:
                context = {
                        'status':False,
                        'text':'Item not found'
                    }
                return JsonResponse(context, safe=True)

    def clear_cart(request):
        if not request.user.is_authenticated or request.user.is_active is False: 
            return redirect('user_app:user_login')
        
        try:
            owner_obj = Owner.objects.get(customer=request.user)
            cart_obj = Order.objects.filter(order_customer=owner_obj, status=0)
            if cart_obj:
                cart_obj.delete()
                context = {
                    'status': True,
                    'text': 'All cart items cleared'
                }
                return JsonResponse(context, safe=True)
            else:
                context = {
                    'status': True,
                    'text': 'Items not found'
                }
                return JsonResponse(context)
        except Exception as e:
            context = {
                    'status': True,
                    'text': 'Items not found in the cart list'
               }
            return JsonResponse(context)


    def update_subtotal(request):
            total = 0
            try:
                owner_obj = Owner.objects.get(customer=request.user)
                cart_obj = Order.objects.filter(order_customer=owner_obj, status=0)
                for item in cart_obj:
                    if item.offer_object is not None:
                        discount_price = (item.product.price + int(item.storage.price_of_size)) * item.offer_object.discount_percentage / 100
                        product_price = (item.product.price + int(item.storage.price_of_size)) - discount_price
                        total += product_price * item.quantity
                        item.total_price = product_price * item.quantity
                        item.save()
                    else:
                        product_price = (item.product.price + int(item.storage.price_of_size)) - item.product.discount_price
                        total += product_price * item.quantity
                        item.total_price = product_price * item.quantity
                
                context = {
                    'status': True,
                    'total': round(total)
                }
                return JsonResponse(context, safe=True)
            except Exception as e:
                context = {
                    'status': False,
                }
                return JsonResponse(context, safe=True)


