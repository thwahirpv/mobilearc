from django.http import JsonResponse
from django.shortcuts import redirect, render
from admin_product_app.models import category, brands, products, Colors, Images, Storage
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


def product_list(request):
    print('haii iam here ..............')
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    
    page = request.GET.get('page', 1)
    products_data = products.objects.filter(colors__isnull=False).distinct()
    category_data = category.objects.all()
   
    # Filter data basaed on category
    if request.GET:
        x = request.GET.get('x', None)
        print(x)
        if x == 'all':
            print('haaaaaaai')
            products_data = products_data.filter(colors__isnull=False).distinct()
        else:
            products_data = products_data.filter(pro_category__category_name=x)

    # Pagination section 
    paginator_obj = Paginator(products_data, 9)
    try:
        products_data = paginator_obj.get_page(page)
    except PageNotAnInteger:
        products_data = paginator_obj.page(1)
    except EmptyPage:
        products_data = paginator_obj.page(paginator_obj.num_pages)

    context={'products_data':products_data, 'category_data':category_data}
    return render(request, 'user_template/list_products.html', context)


def product_view(request, id):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    product_obj = get_object_or_404(products, product_id=id)
    color_obj = Colors.objects.filter(product=product_obj)
    color_id = color_obj[0].color_id
    context={'product_obj':product_obj, 'color_obj':color_obj, 'color_id':color_id}
    return render(request, 'user_template/product_view.html', context)




def collect_image(request, colorId=None, id=None):
    if not request.user.is_authenticated or request.user.is_active is False:
        return redirect('user_app:user_login')
    color_obj = get_object_or_404(Colors, color_id=colorId)
    images = Images.objects.filter(color=color_obj)
    image_data = [{'id':color_obj.color_id, 'link':image.product_image.url} for image in images]
    return JsonResponse({'image_data':image_data}, safe=True)

