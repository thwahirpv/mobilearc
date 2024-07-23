from django.http import JsonResponse
from django.shortcuts import redirect, render
from admin_product_app.models import category, brands, products, Colors, Images, Storage, Wishlist
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import uuid
import json
from django.utils import timezone
from checkout_app.models import review
from django.db.models import Prefetch
from cart_app.models import Owner, Order
from offer_app.models import category_offer, brand_offer


def product_list(request):
    page = request.GET.get('page', 1)
    products_data = products.objects.filter(
        Q(colors__isnull=False) and Q(product_active=True)).distinct()
    category_data = category.objects.filter(category_active=True)
    brand_data = brands.objects.filter(brand_active=True)
    colors_data = Colors.objects.all().distinct()
    sort_by = ''
    show_by = ''
    search = ''
    sort_with_search = ''
    brand = None
    cate = None
    color = None


    # Filter data basaed on category
    if request.GET:
        cate = request.GET.get('cate', None)
        brand = request.GET.get('brand', None)
        color = request.GET.get('color', None)
        sort_by = request.GET.get('sort_by', None)
        show_by = request.GET.get('show_by', None)

        products_data = products.objects.filter(
        Q(colors__isnull=False) and Q(product_active=True)).distinct()

        # getting price from req
        try:
            price = int(request.GET.get('price', 0))
        except:
            price = 0

        # getting search keyword from req
        search = request.GET.get('search_text', None)
        sort_with_search = request.GET.get('sort_with_search', None)
        
        # filter based on category
        if cate is not None:
            if cate == 'all':
                products_data = products_data.filter(
                    colors__isnull=False).distinct()
            else:
                products_data = products_data.filter(
                    pro_category__category_name=cate)
                
        #  filter based on brand
        if brand is not None:
            if brand == 'all':
                products_data = products_data.filter(
                    colors__isnull=False).distinct()
            else:
                products_data = products_data.filter(
                    pro_brand__brand_name=brand)
                
                
        # filter based on color
        if color is not None:
            if color == 'all':
                products_data = products_data.filter(
                    Q(colors__isnull=False)).distinct()
                if sort_with_search:
                    products_data = products_data.filter(product_name__icontains=sort_with_search)
            else:
                products_data = products_data.filter(colors__color_name=color)
                if sort_with_search:
                    products_data = products_data.filter(product_name__icontains=sort_with_search)
        
        # filter based on price
        if price is not 0:
            products_data = products_data.filter(price__lte=price)

        # filter based on search
        if search is not None:
            products_data = products_data.filter(
                product_name__icontains=search)
            sort_with_search = search
            
        # filter based on sorting data
        if sort_by is not None:
            if sort_by == 'all':
                products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True)).all()
                if sort_with_search is not None:
                    products_data = products_data.filter(product_name__icontains=sort_with_search)
            elif sort_by == 'low_to_high':
                products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True)).all().order_by('price')
                if sort_with_search is not None:
                    products_data = products_data.filter(product_name__icontains=sort_with_search)
            elif sort_by == 'high_to_low':
                products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True)).all().order_by('-price')
                if sort_with_search is not None:
                    products_data = products_data.filter(product_name__icontains=sort_with_search)
            elif sort_by == 'new':
                products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True)).all().order_by('-created_at')
                if sort_with_search is not None:
                    products_data = products_data.filter(product_name__icontains=sort_with_search)
        
        # filter based on number of data wnat to show
        if show_by is not None:
            if show_by == 'all':
                if sort_with_search is not None:
                    products_data = products.objects.filter(Q(colors__isnull=False) and Q(product_active=True) and Q(product_name__icontains=sort_with_search)).all()
                else:
                    products_data = products.objects.filter(Q(colors__isnull=False) and Q(product_active=True)).all()
            elif show_by == 'one':
                if sort_with_search is not None:
                    products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True) and Q(product_name__icontains=sort_with_search)).all()[:1]
                else:
                    products_data = products.objects.filter(Q(colors__isnull=False) and Q(product_active=True)).all()[:1]
            elif show_by == 'two':
                if sort_with_search is not None:
                    products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True) and Q(product_name__icontains=sort_with_search)).all()[:2]
                else:
                    products_data = products.objects.filter(Q(colors__isnull=False) and Q(product_active=True)).all()[:2]
            elif show_by == 'three':
                if sort_with_search is not None:
                    products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True) and Q(product_name__icontains=sort_with_search)).all()[:3]
                else:
                    products_data = products.objects.filter(Q(colors__isnull=False) and Q(product_active=True)).all()[:3]
            elif show_by == 'four':
                if sort_with_search is not None:
                    products_data = products_data.filter(Q(colors__isnull=False) and Q(product_active=True) and Q(product_name__icontains=sort_with_search)).all()[:4]
                else:
                    products_data = products.objects.filter(Q(colors__isnull=False) and Q(product_active=True)).all()[:4]
            
        


    # Pagination section
    paginator_obj = Paginator(products_data, 9)
    try:
        products_data = paginator_obj.get_page(page)
    except PageNotAnInteger:
        products_data = paginator_obj.page(1)
    except EmptyPage:
        products_data = paginator_obj.page(paginator_obj.num_pages)

    context = {
        'products_data': products_data,
        'category_data': category_data,
        'brand_data': brand_data,
        'colors_data': colors_data,
        'sort_by':sort_by,
        'show_by':show_by,
        'search':search,
        'sort_with_search':sort_with_search,
        'brand':brand,
        'cate':cate,
        'color':color
    }
    return render(request, 'user_template/list_products.html', context)


def product_view(request, id):
    product_obj = get_object_or_404(products, product_id=id)
    colors_obj = Colors.objects.filter(product=product_obj)
    color_obj = colors_obj[0]

    try:
        review_data = review.objects.filter(
            product=product_obj,
            customer=request.user
        )
    except:
        review_data = review.objects.none()

    context = {
        'product_obj': product_obj,
        'colors_obj': colors_obj,
        'color_obj': color_obj,
        'review_data': review_data
    }
    return render(request, 'user_template/product_view.html', context)

def set_product_price(product_obj, size_of_price):
    global total_price, discount_percentage, offer_id, offer_type, discount_price
    current_time = timezone.now()
    offer_of_category = category_offer.objects.filter(
        Q(offer_category=product_obj.pro_category) & Q(eligible_price__lt=product_obj.price) & Q(is_active=True) & Q(expiration_date__gt=current_time) 
    ).first()

    offer_of_brand = brand_offer.objects.filter(
        Q(brand=product_obj.pro_brand) & Q(eligible_price__lt=product_obj.price) & Q(is_active=True) & Q(expiration_date__gt=current_time)
    ).first()

    if offer_of_category:
        discount_price = ((product_obj.price + size_of_price) * offer_of_category.discount_percentage) / 100
        total_price = (product_obj.price + size_of_price) - discount_price
        discount_percentage = offer_of_category.discount_percentage
        offer_id = offer_of_category.offer_id
        offer_type = 'category'
    elif offer_of_brand:
        discount_price = ((product_obj.price + size_of_price) * offer_of_brand.discount_percentage) / 100
        total_price = (product_obj.price + size_of_price) - discount_price
        discount_percentage = offer_of_brand.discount_percentage
        offer_id = offer_of_brand.offer_id
        offer_type = 'brand'
    else:
        total_price = (product_obj.price + size_of_price) - product_obj.discount_price
        discount_percentage = product_obj.discount_price / total_price * 100
        offer_id = 0
        offer_type = 'product'
        discount_price = 0
    return {
        'total_price':round(total_price),
        'discount_price':round(discount_price),
        'discount_percentage':round(discount_percentage),
        'offer_id':offer_id,
        'offer_type':offer_type
    }
   


def collect_image(request, colorId=None, id=None):
    color_obj = get_object_or_404(Colors, color_id=colorId)
    product_obj = color_obj.product
    storages = Storage.objects.filter(color=color_obj)
    images = Images.objects.filter(color=color_obj)
    image_data = [{'id': color_obj.color_id,
                   'link': image.product_image.url} 
                   for image in images
                ]
    storage_data = [
        {
            'id': storage.size_id,
            'ram': storage.ram,
            'rom': storage.rom,
            'stock': storage.stock,
            'size_price': storage.price_of_size,
            'offer_id': set_product_price(product_obj, int(storage.price_of_size))['offer_id'],
            'offer_type':set_product_price(product_obj, int(storage.price_of_size))['offer_type'],
            'orginal_price': product_obj.price + int(storage.price_of_size),
            'price': set_product_price(product_obj, int(storage.price_of_size))['total_price'],
            'percentage': set_product_price(product_obj, int(storage.price_of_size))['discount_percentage'],
            'discount_price': set_product_price(product_obj, int(storage.price_of_size))['discount_price']
        }  for storage in storages]
    cart_details = {
        'color_id': color_obj.color_id
    }
    return JsonResponse({'image_data': image_data, 'storage_data': storage_data, 'cart_details': cart_details}, safe=True)


def quantity_check(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        storage_id = data.get('storage_id')
        quantity = int(data.get('quantity'))

        try:
            storage_obj = Storage.objects.get(size_id=storage_id)
        except Exception as e:
            pass

        if storage_obj:
            if storage_obj.stock < quantity:
                context = {
                    'status': False,
                    'text': 'out of stock'
                }
                return JsonResponse(context, safe=True)
            else:
                context = {
                    'status': True,
                    'text': 'stock in'
                }
                return JsonResponse(context, safe=True)


# ============Wishlist start======================
class wishlist_management:
    def wishlist_view(request):
        context = {}
        i = 0
        if request.user.is_authenticated:
            wishlist_item = Wishlist.objects.filter(
                user_id=request.user.user_id)
            context = {
                'wishlist_item': wishlist_item
            }
        else:
            wishlist_item = {}
            session_id = request.COOKIES.get('wishlist_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                response = render(
                    request, 'user_template/wishlist.html', {'wishlist_items': []})
                response.set_cookie('wishlist_session_id',
                                    session_id,  max_age=3600)
            wishlist_data = request.session.get(session_id, [])
            for item in wishlist_data:
                product = products.objects.get(product_id=item['product'])
                color = Colors.objects.get(color_id=item['color'])
                storage = Storage.objects.get(size_id=item['storage'])
                items = {
                    'item'+str(i): {
                        'product_id': product.product_id,
                        'color_id':color.color_id,
                        'storage_id':storage.size_id,
                        'image': color.images.first().product_image.url,
                        'name': product.product_name,
                        'color_name':color.color_name,
                        'categroy': product.pro_category.category_name,
                        'brand': product.pro_brand.brand_name,
                        'price': set_product_price(product, int(storage.price_of_size))['total_price'],
                        'storage': storage.rom+'/'+storage.ram
                    }
                }
                i += 1
                wishlist_item.update(items)
            i = 0
            context = {
                'wishlist_item': wishlist_item
            }
        return render(request, 'user_template/wishlist.html', context)

    def add_wishlist_item(request, id):
        if request.method == 'POST':
            print('this is post')
            color_id = request.POST.get('color_id')
            storage_id = request.POST.get('storage_id')
            context = {}
            color_obj = Colors.objects.get(color_id=color_id)
            storage_obj = Storage.objects.get(size_id=storage_id)
            product_obj = color_obj.product
            print('iam complete taking details')

            try:
                print('starting authentication')
                if request.user.is_authenticated:
                    wishlist_item, created = Wishlist.objects.get_or_create(
                        user=request.user,
                        product=product_obj,
                        color=color_obj,
                        storage=storage_obj
                    )
                    context = {
                        'status': True
                    }
                    print('Iam finish the creatingq')
                else:
                    session_id = request.COOKIES.get('wishlist_session_id')
                    if not session_id:
                        session_id = str(uuid.uuid4())
                        response = JsonResponse({'success': True})
                        response.set_cookie(
                            'wishlist_session_id', session_id,  max_age=3600)
                        return response

                    wishlist = request.session.get(session_id, [])
                    if not any(item.get('product') == product_obj.product_id and 
                        item.get('color') == color_obj.color_id and 
                        item.get('storage') == storage_obj.size_id 
                        for item in wishlist):
                        wishlist.append({
                            'user': session_id,
                            'product': product_obj.product_id,
                            'color':color_obj.color_id,
                            'storage':storage_obj.size_id
                        })
                        request.session[session_id] = wishlist
                    context = {
                        'status': True
                    }
            except:
                context = {
                    'status': False
                }
            print('hello iam near the return                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ')
            return JsonResponse(context, safe=True)

    def remove_from_wishlist(request, p_id, c_id=None, s_id=None):
        context = {}
        if request.user.is_authenticated:
            try:
                wishlist_obj = Wishlist.objects.get(wishlist_id=p_id)
                if wishlist_obj:
                    wishlist_obj.delete()
                    context = {
                        'status': True,
                        'text': f'{wishlist_obj.product.product_name} is removed'
                    }
                    return JsonResponse(context, safe=True)
                else:
                    context = {
                        'status': False,
                        'text': 'item not exits!'
                    }
                return JsonResponse(context, safe=True)

            except Exception as e:
                context = {
                    'status': False,
                    'text': 'item not exits!'
                }
                return JsonResponse(context, safe=True)
        else:
            session_id = request.COOKIES.get('wishlist_session_id')
            product_obj = products.objects.get(product_id=p_id)
            color_obj = Colors.objects.get(color_id=c_id)
            storage_obj = Storage.objects.get(size_id=s_id)
            if session_id:
                wishlist_data = request.session.get(session_id, [])
                for i, item in enumerate(wishlist_data):
                    if item['product'] == p_id and item['color'] == c_id and item['storage'] == s_id:
                        del wishlist_data[i]
                        break
                request.session[session_id] = wishlist_data
                request.session.modified = True
                context = {
                    'status': True,
                    'text': f'{product_obj.product_name} is removed'
                }
                return JsonResponse(context, safe=True)

    def move_to_cart(request):
        if not request.user.is_authenticated or request.user.is_active is False:
            return redirect('user_app:user_login')
        wishlist_id = request.POST.get('wishlist_id')
        try:
            wishlist_obj = Wishlist.objects.get(wishlist_id=wishlist_id)
        except:
            context = {
                'status': False
            }
            JsonResponse(context, safe=True)

        try:
            owner_obj, owner_created = Owner.objects.get_or_create(
                customer=request.user
            )

            order_Obj, cart_created = Order.objects.get_or_create(
                order_customer=owner_obj,
                product=wishlist_obj.product,
                color=wishlist_obj.color,
                storage=wishlist_obj.storage,
                status=0
            )
            wishlist_obj.delete()
            context = {
                'status': True
            }
            return JsonResponse(context, safe=True)
        except:
            context = {
                'status': False
            }
            return JsonResponse(context, safe=True)


# ===========Wishlist End=========================
