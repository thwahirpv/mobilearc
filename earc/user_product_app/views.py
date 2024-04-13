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


def product_list(request):
    
    page = request.GET.get('page', 1)
    products_data = products.objects.filter(Q(colors__isnull=False) and Q(product_active=True)).distinct()
    category_data = category.objects.filter(category_active=True)
    brand_data = brands.objects.filter(brand_active=True)
    colors_data = Colors.objects.all().distinct()
    print('first', products_data.count())
   
    # Filter data basaed on category
    if request.GET:
        cate = request.GET.get('cate', None)
        brand = request.GET.get('brand', None)
        color = request.GET.get('color', None)
        try:
            price = int(request.GET.get('price', 0))
        except:
            price = 0
        search = request.GET.get('search_text', None)

        if cate is not None:
            if cate == 'all':
                products_data = products_data.filter(colors__isnull=False).distinct()
            else:
                products_data = products_data.filter(pro_category__category_name=cate)
        elif brand is not None:
            if brand == 'all':
                products_data = products_data.filter(colors__isnull=False).distinct()
            else:
                products_data = products_data.filter(pro_brand__brand_name=brand)
        elif color is not None:
            if color == 'all':
                products_data = products_data.filter(colors__isnull=False).distinct()
            else:
                products_data = products_data.filter(colors__color_name=color)
        elif price is not 0:
            products_data = products_data.filter(price__lte=price)
        elif search is not None:
            products_data = products_data.filter(product_name__icontains=search)

    # Pagination section 
    paginator_obj = Paginator(products_data, 9)
    try:
        products_data = paginator_obj.get_page(page)
    except PageNotAnInteger:
        products_data = paginator_obj.page(1)
    except EmptyPage:
        products_data = paginator_obj.page(paginator_obj.num_pages)

    context={
        'products_data':products_data, 
        'category_data':category_data,
        'brand_data':brand_data,
        'colors_data':colors_data
    }
    return render(request, 'user_template/list_products.html', context)


def product_view(request, id):
    product_obj = get_object_or_404(products, product_id=id)
    colors_obj = Colors.objects.filter(product=product_obj)
    color_obj = colors_obj[0]
    context={
        'product_obj':product_obj, 
        'colors_obj':colors_obj,
        'color_obj':color_obj
    }
    return render(request, 'user_template/product_view.html', context)




def collect_image(request, colorId=None, id=None):
    color_obj = get_object_or_404(Colors, color_id=colorId)
    product_obj = color_obj.product
    storages = Storage.objects.filter(color=color_obj)
    images = Images.objects.filter(color=color_obj)
    image_data = [{'id':color_obj.color_id, 'link':image.product_image.url} for image in images]
    storage_data =[
        {'ram':storage.ram, 
         'rom':storage.rom, 
         'stock':storage.stock, 
         'size_price':storage.price_of_size, 
         'price':product_obj.price+int(storage.price_of_size),
         'percentage':product_obj.get_discount_percentage(size_Price=storage.price_of_size)
         } for storage in storages]
    return JsonResponse({'image_data':image_data, 'storage_data':storage_data}, safe=True)




# ============Wishlist start======================
class wishlist_management:
    def wishlist_view(request):
        context = {}
        i = 0
        if request.user.is_authenticated:
            wishlist_item = Wishlist.objects.filter(user_id=request.user.user_id)
            context = { 
                'wishlist_item':wishlist_item
            }
        else:
            wishlist_item = {}
            session_id = request.COOKIES.get('wishlist_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                response = render(request, 'user_template/wishlist.html', {'wishlist_items':[]})
                response.set_cookie('wishlist_session_id', session_id,  max_age=3600)
            wishlist_data = request.session.get(session_id, [])
            for item in wishlist_data:
                product = products.objects.get(product_id=item['product'])
                items = {
                    'item'+str(i): {
                        'id':product.product_id,
                        'image':product.thumbnail.url,
                        'name':product.product_name,
                        'categroy':product.pro_category.category_name,
                        'brand':product.pro_brand.brand_name,
                        'price':product.price,
                    }
                }
                i += 1
                wishlist_item.update(items)
            i=0
            context = {
                'wishlist_item':wishlist_item 
            }
        return render(request, 'user_template/wishlist.html', context)
    
    def add_wishlist_item(request, id):
        context = {}
        product_obj = get_object_or_404(products, product_id=id)
        try:
            if request.user.is_authenticated:
                wishlist_item, created = Wishlist.objects.get_or_create(
                    user=request.user,
                    product=product_obj
                )
                context = {
                    'status': True
                }
            else:
                session_id = request.COOKIES.get('wishlist_session_id')
                if not session_id:
                    session_id =  str(uuid.uuid4())
                    response = JsonResponse({'success':True})
                    response.set_cookie('wishlist_session_id', session_id,  max_age=3600)
                    return response
                
                
                wishlist = request.session.get(session_id, [])
                if not any(item.get('product') == product_obj.product_id for item in wishlist):
                    wishlist.append({
                        'user':session_id,
                        'product':product_obj.product_id
                    })
                    request.session[session_id] = wishlist
                context = {
                    'status': True
                } 
        except: 
            context = {
                'status': False
            }
        return JsonResponse(context, safe=True)
    

    def remove_from_wishlist(request, id):
        context = {}
        if request.user.is_authenticated:
            try:
                wishlist_obj = Wishlist.objects.get(wishlist_id=id)
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
            product_obj = products.objects.get(product_id=id)
            if session_id:
                wishlist_data = request.session.get(session_id, [])
                for i, item in enumerate(wishlist_data):
                    if item['product'] == id:
                        print('hellllllllllllllll')
                        del wishlist_data[i]
                        break
                request.session[session_id] = wishlist_data
                request.session.modified = True
                context = {
                        'status': True, 
                        'text': f'{product_obj.product_name} is removed'
                    }
                return JsonResponse(context, safe=True)

                    


            

# ===========Wishlist End=========================


