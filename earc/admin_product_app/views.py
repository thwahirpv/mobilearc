import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import category, brands, products, Colors, Images, Storage
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.db.models import F, Sum, Count, ExpressionWrapper, IntegerField
from django.db.models import Max, Prefetch
# ==================================================================================================================


#=========================================== start Category management ====================================================
class category_management:


    # category lising and add new category
    @never_cache
    def category(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')
            image = request.FILES.get('category_image')


            if image:
                try:
                   file_content = image.read()
                   img = Image.open(BytesIO(file_content))
                   if not img.format.lower() in ['jpeg', 'jpg', 'png']:
                       messages.error(request, 'Invalid formate, upload jpeg or png')
                       return redirect('admin_product_app:admin_category')
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect('admin_product_app:admin_category')
            else:
                messages.error(request, 'Upload image!')
                return redirect('admin_product_app:admin_category')


            if name == '' or discription == '':
                messages.error(request, 'Fill those fields!')
                return redirect('admin_product_app:admin_category')
            elif not type(name) == str and type(discription) == str:
                messages.error(request, 'Enter meaningfull details!')
                return redirect('admin_product_app:admin_category')
            elif name.isspace() or discription.isspace():
                messages.error(request, 'Enter valid details!')
                return redirect('admin_product_app:admin_category')
            elif len(name) < 2 or len(discription) < 1:
                messages.error(request, 'Enter valid details!')
                return redirect('admin_product_app:admin_category')
            elif category.objects.filter(category_name=name).exists():
                messages.error(request, f'{name} is already exist')
                return redirect('admin_product_app:admin_category')
            else:
                category.objects.create(category_name=name, category_disc=discription, category_image=image)
                return redirect('admin_product_app:admin_category')
        categories = category.objects.all()
        context = {'cotegories':categories}
        return render(request, 'admin_template/page-categories.html', context)
    
    # category delete
    @never_cache
    def delete_category(request, id):
        category_obj = get_object_or_404(category, category_id=id)
        category_obj.delete()
        return redirect('admin_product_app:admin_category')
    
    # category update
    @never_cache
    def update_category(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        category_obj = get_object_or_404(category, category_id=id)
        reverse_url = reverse('admin_product_app:update_category', kwargs={'id':id})

        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')
            image = request.FILES.get('category_image', category_obj.category_image)  

            if image:
                try:
                    file_content = image.read()
                    img = Image.open(BytesIO(file_content))
                    if not img.format.lower() in ['jpg', 'jpeg', 'png']:
                        messages.error(request, 'Invalid file. Upload jpeg or jpg')
                        return redirect(reverse_url)
                except:
                    messages.error(request, 'invalid file!')
                    return redirect(reverse_url)
            else:
                messages.error(request, 'upload Image!')
                return redirect(reverse_url)

            if name == '' or discription == '':
                messages.error(request, 'Fill those fields!')
                return redirect(reverse_url)
            elif not type(name) == str or not type(discription) == str:
                messages.error(request, 'Enter meaningfull details!')
                return redirect(reverse_url)
            elif name.isspace() or discription.isspace():
                messages.error(request, 'Enter valid details!')
                return redirect(reverse_url)
            elif len(name) < 2 or len(discription) < 1:
                messages.error(request, 'Enter valid details!')
                return redirect(reverse_url)
            elif not name == category_obj.category_name:
                if category.objects.filter(category_name=name).exists():
                    messages.error(request, f'{name} is already exists!')
                    return redirect(reverse_url)
            
            category_obj.category_name = name
            category_obj.category_disc = discription
            category_obj.category_image = image
            category_obj.save()               
            return redirect('admin_product_app:admin_category')
        return render(request, 'admin_template/page-update-category.html', {'category_obj':category_obj})
    
    # category block and unblock
    
    def block_and_unblock(request, action, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        category_obj = get_object_or_404(category, category_id=id)

        if action == 'get_name':
            context = {
                'name':category_obj.category_name
            }
            return JsonResponse(context, safe=True)
        
        elif action == 'block':
            category.objects.filter(category_id=id).update(category_active=False)
            brands.objects.filter(brand_category=category_obj).update(brand_active=False)
            products.objects.filter(pro_category=category_obj).update(product_active=False)
            context = {
                'status':'success',
                'title':'Blocked',
                'text':f"{category_obj.category_name} is Blocked"
            }
            return JsonResponse(context, safe=True)
        
        elif action == 'unblock':
            if 'brand_id' in request.session:
                brand_id = request.session.get('brand_id')
                brand_obj = get_object_or_404(brands, brand_id=brand_id)
                brand_obj.brand_active = True
                brand_obj.save()
                del request.session['brand_id']

            if 'product_id' in request.session:
                product_id = request.session.get('product_id')
                product_obj = get_object_or_404(products, product_id=product_id)
                product_obj.product_active = True
                product_obj.save()
                del request.session['product_id']

            category.objects.filter(category_id=id).update(category_active=True)

            context = {
                'status':'success',
                'category':category_obj.category_name, 
                'title':'Unblocked',
                'text':f"{category_obj.category_name} is Unblocked"
            }
            return JsonResponse(context, safe=True)
#=========================================== end Category management ====================================================



#=========================================== start brand management ====================================================    
# brand management
class brand_management:
    # list all brands
    def brands(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        name = request.GET.get('category', None)
        status = request.GET.get('status', None)
        brands_data = brands.objects.all() 
        status_data = 'All'
        category_name = 'category'
        if status is not None:
            if 'All' in status:
                brands_data = brands.objects.all() 
            elif 'Active' in status:
                brands_data = brands.objects.filter(brand_active=True)
                status_data = 'Active'
            elif 'Blocked' in status:
                brands_data = brands.objects.filter(brand_active=False)
                status_data = 'Blocked'
        else:  
            if name is None: 
                pass
            elif 'all' in name:
                category_name = name
            elif category_name is not None:
                brands_data = brands.objects.filter(brand_category__category_name=name)
                category_name = name
        categories = category.objects.all()
        context = {'categories':categories, 'brands_data':brands_data, 'category_name': category_name, 'status_data':status_data}
        return render(request, 'admin_template/page-brands.html', context)
    
    # add new brand
    @never_cache
    def add_brand(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        if request.method == 'POST':   
            name = request.POST.get('name')
            brand_image = request.FILES.get('brand_image')
            category_name = request.POST.get('category')

            # Check if any category is empty 
            if name == '' or category_name == '':
                messages.error(request, 'Fill all fields!')
                return redirect('admin_product_app:add_brand')
            
            # Check image field 
            if brand_image:
                try:
                    file_content = brand_image.read()
                    image = Image.open(BytesIO(file_content))
                    if not image.format.lower() in ['jpeg', 'jpg', 'png']:
                        messages.error(request, 'invalid image formate!. upload jpeg or png')
                        return redirect('admin_product_app:add_brand')
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect('admin_product_app:add_brand')
            else:
                messages.error(request, 'upload image!')
                return redirect('admin_product_app:add_brand')
            
            # Check brand name is string
            if not type(name) == str:
                messages.error(request, 'Enter meaningfull details!')
                return redirect('admin_product_app:add_brand')
            
            # Check only space 
            elif name.isspace() or category_name.isspace():
                messages.error(request, 'Enter valid details!')
                return redirect('admin_product_app:add_brand')
            
            # Check brand_name lenght 
            elif len(name) < 3 :
                messages.error(request, f'{name} is not valid!')
                return redirect('admin_product_app:add_brand')
            
            # Check brand_name is already exists
            elif brands.objects.filter(brand_name=name).exists():
                messages.error(request, f'{name} is already exits')
                return redirect('admin_product_app:add_brand')
            
            # Create brand
            else:
                category_obj = get_object_or_404(category, category_name=category_name)
                brand_obj = brands.objects.create(brand_name=name, brand_image=brand_image, brand_category=category_obj)
                if category_obj.category_active is False:
                    brand_obj.brand_active = False
                    brand_obj.save()
                return redirect('admin_product_app:list_brands')
        categories = category.objects.all()
        return render(request, 'admin_template/page-addbrand.html', {'categories':categories})
    
    # Edit brand
    @never_cache
    def update_brand(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        categories = category.objects.all()
        brand = get_object_or_404(brands, brand_id=id)
        if request.method == 'POST':
            name = request.POST.get('name')
            image = request.FILES.get('brand_image', brand.brand_image)
            category_name = request.POST.get('category')
            category_obj = get_object_or_404(category, category_name=category_name)

            # Check image
            if image:
                try:
                    file_content = image.read()
                    brand_img = Image.open(BytesIO(file_content))
                    if not brand_img.format.lower() in ['jpeg', 'jpg', 'png']:
                        messages.error(request, 'invalid image formate!. upload jpeg or png')
                        return redirect('admin_products_app:update_brand')
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect('admin_product_app:update_brand')
            else:
                messages.error(request, 'upload image!')
                return redirect('admin_product_app:update_brand')

            if name == '' or category_name == '':
                messages.error(request, 'Fill those fields!')
                return redirect('admin_product_app:update_brand')

            if not type(name) == str:
                messages.error(request, 'Enter meaningfull details!')
                return redirect('admin_product_app:update_brand')
            elif name.isspace() or category_name.isspace():
                messages.error(request, 'Enter valid details!')
                return redirect('admin_product_app:update_brand')
            elif len(name) < 3:
                messages.error(request, 'Enter valid details!')
                return redirect('admin_products_app:update_brand')
            else:
                brand.brand_name = name
                brand.brand_image = image
                brand.brand_category = category_obj
                brand.save()
                brand_obj = get_object_or_404(brands, brand_id=brand.brand_id)
                products.objects.filter(pro_brand=brand_obj).update(pro_brand=brand_obj)
                return redirect('admin_product_app:list_brands')
        context = {'categories':categories, 'brand':brand }
        return render(request, 'admin_template/page-brandupdate.html', context)

    # Brand block and unblock
   
    def block_and_unblock(request, action, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        brand_obj = get_object_or_404(brands, brand_id=id)
        if action == 'get_name':
            name = brand_obj.brand_name
            context = {'name':name,'brand_id':brand_obj.brand_id,}
            return JsonResponse(context, safe=True)
        elif action == 'block':
            brands.objects.filter(brand_id=id).update(brand_active=False)
            products.objects.filter(pro_brand=brand_obj).update(product_active=False)
            context = {
                'status':'success', 
                'name':brand_obj.brand_name,
                'title':'Blocked',
                'brand_id':brand_obj.brand_id,
                'text':f'{brand_obj.brand_name} Brand is Blocked'
                }
            return JsonResponse(context, safe=True)
        elif action == 'unblock':
            category_status = brand_obj.brand_category.category_active
            if category_status: 
                if 'product_id' in request.session:
                    product_id = request.session.get('product_id')
                    product_obj = get_object_or_404(products, product_id=product_id)
                    product_obj.product_active = True
                    product_obj.save()
                    del request.session['product_id']

                brands.objects.filter(brand_id=id).update(brand_active=True)
                
                context = {
                    'status':'success',
                    'name':brand_obj.brand_name,
                    'title':'Unblocked',
                    'brand_id':brand_obj.brand_id,
                    'text':f'{brand_obj.brand_name} Brand is Unblocked'
                }
                return JsonResponse(context, safe=True)
            else:
                request.session['brand_id'] = brand_obj.brand_id
                context = {
                    'status':'warning',
                    'name':brand_obj.brand_name,
                    'title':'failed',
                    'category':brand_obj.brand_category.category_name,
                    'category_id':brand_obj.brand_category.category_id,
                    'brand_id':brand_obj.brand_id,
                    'text':f"Category of {brand_obj.brand_name} is still blocked. if you want unblock {brand_obj.brand_name} first you want to unblock {brand_obj.brand_category.category_name}."
                }
                return JsonResponse(context, safe=True)
            


    # delete brand
    @never_cache
    def delete_brand(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        brand_obj = get_object_or_404(brands, brand_id=id)
        brand_obj.delete()
        return redirect('admin_product_app:list_brands')
#=========================================== end brand management ====================================================



#=========================================== start product management ================================================  
# product management 
class product_management:

    

    # show all prosucts 
    def list_products(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        product_data = products.objects.all()
        name = request.GET.get('brand', None)
        status = request.GET.get('status', None)
        status_data = 'All'
        brand_name = 'All Brands'

        # Filter Active and Blocked products
        if status is not None:
            if 'All' in status:
                pass
            elif 'Active' in status:
                product_data = product_data.filter(product_active=True)
                status_data = 'Active'
            elif 'Blocked' in status:
                product_data = product_data.filter(product_active=False)
                status_data = 'Blocked'
        # Filter brand base products
        else:
            if name is None:
                pass
            elif 'all' in name:
                brand_name = 'All Brands'
            elif name is not None:
                product_data = product_data.filter(pro_brand__brand_name=name)
                brand_name = name
        brands_data = brands.objects.all()
        

        context = {'product_data':product_data, 'brands_data':brands_data, 'brand_name':brand_name, 'status_data':status_data}
        return render(request, 'admin_template/page-products-list.html', context)

    # add new product  
    def add_product(request):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        if request.method == 'POST':
            thumbnail = request.FILES.get('thumbnail')
            product_name = request.POST.get('product_name')
            product_disc = request.POST.get('product_dic')
            try:
                product_price = int(request.POST.get('price'))
                product_diacount_price = int(request.POST.get('discount_price'))
            except:
                messages.error(request, 'Enter correct price!')
                return redirect('admin_product_app:add_product')
            product_category = request.POST.get('product_category')
            product_brand = request.POST.get('product_brand')

            # product name validation 
            if product_name == '' or product_name.isspace() or product_name.isdigit():
                messages.error(request, 'Enter valid name!')
                return redirect('admin_product_app:add_product')
            
            # product discription validation
            elif product_disc == '' or product_disc.isspace() or product_disc.isdigit():
                messages.error(request, 'Enter valid Discription!')
                return redirect('admin_product_app:add_product')
            
            elif  product_price < 1:
                messages.error(request, 'Enter valid Price!')
                return redirect('admin_product_app:add_product')

            elif product_diacount_price == product_price or product_diacount_price < 1:
                messages.error(request, 'Enter valid discount price')
                return redirect('admin_product_app:add_product')
            
            # product category validation
            elif product_category == 'Category':
                messages.error(request, 'select category!!')
                return redirect('admin_product_app:add_product')

            # product cateogory validation
            elif product_brand == 'Brand':
                messages.error(request, 'select Brand!')
                return redirect('admin_product_app:add_product')
            
            # check product is exits or not 
            elif products.objects.filter(product_name__icontains=product_name).exists():
                messages.error(request, f'{product_name} is alreay exists')
                return redirect('admin_product_app:add_product')

            category_obj = get_object_or_404(category, category_name=product_category)
            brand_obj = get_object_or_404(brands, brand_name=product_brand)
            product_obj = products.objects.create(thumbnail=thumbnail, product_name=product_name, product_disc=product_disc, price=product_price, discount_price=product_diacount_price, pro_category=category_obj, pro_brand=brand_obj) 
            if brand_obj.brand_active is False:
                product_obj.product_active = False
                product_obj.save()
            return redirect('admin_product_app:list_products')

        brand = brands.objects.all()
        context = {'brand':brand}
        return render(request, 'admin_template/page-product-add.html', context)
    
    # update product
    @cache_control(no_cache=True, must_revalidate=True, max_age=0)
    def update_product(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        product_obj = get_object_or_404(products, product_id=id)
        brands_data = brands.objects.all()
        if request.method == 'POST':
            name = request.POST.get('name', product_obj.product_name)
            discription = request.POST.get('discription', product_obj.product_disc)
            product_image = request.FILES.get('image', product_obj.thumbnail)
            pro_category = request.POST.get('category', product_obj.product_active)
            pro_brand = request.POST.get('brand', product_obj.pro_brand)
            try:
                product_price = int(request.POST.get('price', product_obj.price))
                product_diacount_price = int(request.POST.get('discount_price', product_obj.discount_price))
            except:
                messages.error(request, 'Enter correct price!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))
            


            # image validation
            if product_image:
                try:
                    file_content = product_image.read()
                    image = Image.open(BytesIO(file_content))
                    print(image.format.lower)
                    if not image.format.lower() in ['jpeg', 'jpg', 'png']:
                        messages.error(request, 'invalid image formate!. upload jpeg or png')
                        return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))
            else:
                messages.error(request, 'upload image!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))

            if name == '' or name.isspace() or not type(name) == str:
                messages.error(request, 'Enter valid name!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))

            # product discription validation
            elif discription == '' or discription.isspace() or not type(discription) == str:
                messages.error(request, 'Enter valid Discription!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))
            
            elif  product_price < 1:
                messages.error(request, 'Enter valid Discription!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))

            elif product_diacount_price == product_price or product_diacount_price < 1:
                messages.error(request, 'Enter valid Discription!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))
            
            # product category validation
            elif pro_category == 'Category':
                messages.error(request, 'select category!!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))

            # product cateogory validation
            elif pro_brand == 'Brand':
                messages.error(request, 'select Brand!')
                return redirect(reverse('admin_product_app:update_product', kwargs={'id':id}))
            
            
            
            product_obj.product_name = name
            product_obj.variant_disc = discription
            product_obj.thumbnail = product_image
            product_obj.price = product_price
            product_obj.discount_price = product_diacount_price
            category_obj = get_object_or_404(category, category_name=pro_category)
            product_obj.pro_category = category_obj
            brand_obj = get_object_or_404(brands, brand_name=pro_brand)
            product_obj.pro_brand = brand_obj
            product_obj.save()
            return redirect('admin_product_app:list_products')
        context = {'product_obj':product_obj, 'brands_data':brands_data}
        return render(request, 'admin_template/update-product.html', context)
    
    # product block and unblock 

    def block_and_unblock(request, action, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        product_obj = get_object_or_404(products, product_id=id)
        brand_obj = product_obj.pro_brand

        if action == 'get_name':
            context = {
                'name':product_obj.product_name
            }
            return JsonResponse(context, safe=True)
        
        elif action == 'block':
            product_obj.product_active = False
            product_obj.save()
            context = {
                'status':'success',
                'text':f"{product_obj.product_name} is Blocked",
                'title':'Blocked',
                'name': product_obj.product_name
            }
            return JsonResponse(context, safe=True)
        
        elif action == 'unblock':
            if brand_obj.brand_active:
                product_obj.product_active = True
                product_obj.save()
                context = {
                    'status':'success',
                    'text':f"{product_obj.product_name} is Unblocked",
                    'title':'Unblocked',
                    'name': product_obj.product_name
                }
                return JsonResponse(context, safe=True)
            else:
                request.session['product_id'] = product_obj.product_id
                context = {
                    'status':'warning',
                    'text':f"Brand of {product_obj.product_name} id still blocked. If you want unblock {product_obj.product_name} first you need to unblock {brand_obj.brand_name}",
                    'title':'failed',
                    'brand_id':brand_obj.brand_id,
                    'name':'product_obj.product_name'
                }
                return JsonResponse(context, safe=True)
            

    def delete_product(request, id):
        product_obj = get_object_or_404(products, product_id=id)
        product_obj.delete()
        return redirect('admin_product_app:list_products')
    
    def stock_view(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        stock_obj = products.objects.filter(product_id=id).prefetch_related(
            Prefetch('colors', queryset=Colors.objects.order_by('-color_id').prefetch_related(
                Prefetch('storage', queryset=Storage.objects.order_by('-size_id'), to_attr='storages')
            ), to_attr='colours')
        )    
        context = {
            'stock_obj': stock_obj
        }
        return render(request, 'admin_template/stock_view.html', context)
        
#=========================================== end product management ====================================================



# ========================================= Start Varinat management ===================================================
class variant_management:

    # list variant
    def list_variant(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        product_obj = get_object_or_404(products, product_id=id)
        color_variant = Colors.objects.filter(product=product_obj)
        context={'color_variant':color_variant, 'product_obj':product_obj}
        return render(request, 'admin_template/variant_list.html', context)


    # Add variant
   
    def add_color_variant(request, id=None):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        product_obj = get_object_or_404(products, product_id=id)
        url = reverse('admin_product_app:add_variant', kwargs={'id':id})
        if request.method == 'POST':
            color_name = request.POST.get('color')
            images = request.FILES.getlist('images')

            if color_name == '' or color_name.isspace() or color_name.isdigit():
                messages.error(request, 'Enter valid color!')
                return redirect(url)
               
            if images:
                try:
                    for image in images:
                        file_content = image.read()
                        variant_img = Image.open(BytesIO(file_content))
                        if not variant_img.format.lower() in ['jpeg', 'jpg', 'png']:
                            messages.error(request, 'Invalid image formate! upload jpeg or png')
                            return redirect(url)
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect(url)
            else:
                messages.error(request, 'upload image!')
                return redirect(url)
            
            
            color_obj = Colors.objects.create(color_name=color_name, product=product_obj)
            for index, image in enumerate(images, start=1):
                priority = request.POST.get(f'order_{index}', index)
                Images.objects.create(product_image=image, priority=priority, color= color_obj)
            return redirect('admin_product_app:list_products')
        return render(request, 'admin_template/page-add-variant.html')
    
    def variant_detailed_view(request, id=None):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        color_obj = get_object_or_404(Colors, color_id=id)
        product_id = color_obj.product.product_id
        product_obj = get_object_or_404(products, product_id=product_id)
        context={'color_obj':color_obj, 'product_obj':product_obj}
        return render(request, 'admin_template/variant_detailed_view.html', context)

    def add_variant_image(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        color_obj = get_object_or_404(Colors, color_id=id)
        priority = color_obj.images.count()+1
        fail_url = reverse('admin_product_app:add_varient_image', kwargs={'id':id})
        success_url = reverse('admin_product_app:variant_detailed_view', kwargs={'id':id})

        if request.method == 'POST':
            image_data = request.FILES.get('select_image')

            if image_data:
                try:
                    file_content = image_data.read()
                    variant_image = Image.open(BytesIO(file_content))
                    if not variant_image.format.lower() in ['jpeg', 'jpg', 'png']:
                        messages.error(request, 'invalid image formate!. upload jpeg or png')
                        return redirect(fail_url)
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect(fail_url)
            else:
                messages.error(request, 'upload image!')
                return redirect(fail_url)
            
            Images.objects.create(product_image=image_data, priority=priority, color=color_obj)
            return redirect(success_url)
        return render(request, 'admin_template/change_varinat_image.html')
    
    def delete_image(request, image_id=None, id=None):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        image=get_object_or_404(Images, image_id=image_id)
        image.delete()
        return redirect(reverse('admin_product_app:variant_detailed_view', kwargs={'id':id}))
    
    
    def change_image(request, image_id=None, id=None):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        target_image = get_object_or_404(Images, image_id=image_id)
        failer_url = reverse('admin_product_app:change_image', kwargs={'image_id':image_id, 'id':id})
        success_url = reverse('admin_product_app:variant_detailed_view', kwargs={'id':id})
        if request.method == 'POST':
            image_data = request.FILES.get('select_image')
            
            
            if image_data:
                try:
                    file_content = image_data.read()
                    variant_image = Image.open(BytesIO(file_content))
                    if not variant_image.format.lower() in ['jpeg', 'jpg', 'png']:
                        messages.error(request, 'invalid image formate!. upload jpeg or png')
                        return redirect(failer_url)
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect(failer_url)
            else:
                messages.error(request, 'upload image!')
                return redirect(failer_url)
            
            if Image.open(image_data) == Image.open(target_image.product_image):
                messages.error(request, 'Image already exits!')
                return redirect(failer_url)
            
            target_image.product_image = image_data
            target_image.save()
            return redirect(success_url)
        context={'target_image':target_image}
        return render(request, 'admin_template/change_varinat_image.html', context)
        
    
    def add_storage_variant(request, product_id=None, id=None):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        url = reverse('admin_product_app:add_storage_variant', kwargs={'product_id':product_id,'id':id})
        color_obj = get_object_or_404(Colors, color_id=id)

        if request.method == 'POST':
            price_of_size = request.POST.get('price_of_size')
            stock = int(request.POST.get('stock'))
            rom = request.POST.get('rom')
            ram = request.POST.get('ram')
            

            if price_of_size == '' or price_of_size.isspace() or int(price_of_size) < 1:
                messages.error(request, 'Invalid price!')
                return redirect(url)
            elif stock == '' or stock is None or stock < 0:
                messages.error(request, 'Enter valid stock!')  
                return redirect(url)
            elif rom is None or rom == '' or rom < 2:
                messages.error(request, 'Select one of the Rom!')
                return redirect(url)
            elif ram is None or ram == '' or ram < 2:
                messages.error(request, 'Select one of the Ram!')
                return redirect(url)

            Storage.objects.create(ram=ram, rom=rom, price_of_size=price_of_size, stock=stock, color=color_obj)
            return redirect(reverse('admin_product_app:list_variant', kwargs={'id': product_id}))
        return render(request, 'admin_template/add_storage.html')
    

    def delete_color(request, product_id, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        color_obj = get_object_or_404(Colors, color_id=id)
        color_obj.delete()
        return redirect(reverse('admin_product_app:list_variant', kwargs={'id':product_id}))

    def get_color_name(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        print('i reach this function')
        print(id)
        color_obj = get_object_or_404(Colors, color_id=id)
        if request.method == 'POST':
            try:
                new_name = request.POST.get('new_name')
                print(new_name)
                color_obj.color_name = new_name
                color_obj.save()
                context = {
                    'status':'success',
                }
                return JsonResponse(context, safe=True)
            except Exception:
                context = {
                    'status': 'failed',
                    'text':'someting wrong!'
                }
                return JsonResponse(context, safe=True)
            
    def update_storage(request, id):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        storage_obj = get_object_or_404(Storage, size_id=id)
        color_id = storage_obj.color.color_id
        if request.method == 'POST':
            ram = request.POST.get('ram', storage_obj.ram)
            rom = request.POST.get('rom', storage_obj.rom)
            price = request.POST.get('price', storage_obj.price_of_size)
            stock = request.POST.get('stock', storage_obj.stock)


            if price == '' or price.isspace() or int(price) < 1:
                messages.error(request, 'Invalid price!')
                return redirect(reverse('admin_product_app:edit_storage', kwargs={'id':id}))
            elif stock == '' or stock.isspace() or int(stock) < 0:
                messages.error(request, 'Enter valid stock!')  
                return redirect(reverse('admin_product_app:edit_storage', kwargs={'id':id}))
            elif rom is None or rom.isspace() or int(rom) < 2:
                messages.error(request, 'Select one of the Rom!')
                return redirect(reverse('admin_product_app:edit_storage', kwargs={'id':id}))
            elif ram is None or ram.isspace() or int(ram) < 2:
                messages.error(request, 'Select one of the Ram!')
                return redirect(reverse('admin_product_app:edit_storage', kwargs={'id':id}))
            
            

            storage_obj.ram = ram
            storage_obj.rom = rom 
            storage_obj.price_of_size = price
            storage_obj.stock = stock 
            storage_obj.save()
            return redirect(reverse('admin_product_app:variant_detailed_view', kwargs={'id':color_id}))
        context = {
            'storage_obj':storage_obj
        }
        return render(request, 'admin_template/update_storage.html', context)
   

    def delete_storage(request, id, action):
        if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
        
        storage_obj = get_object_or_404(Storage, size_id=id)
        context = {}
        if action == 'get_name':
            storage_name = storage_obj.rom+'/'+storage_obj.ram
            context = {
                'status': 'success',
                'name': storage_name
            }
            return JsonResponse(context, safe=True)
        else:
            try:
                storage_obj.delete()
                context = {
                    'status':'success',
                    'text':'Successfully Deleted'
                }
            except:
                context = {
                    'status':'failed',
                    'text': 'Deleting is Failed'
                }
            return JsonResponse(context, safe=True)


# fetch brand based on category
def get_category(request, brand_name, id=None):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    brand_obj = get_object_or_404(brands, brand_name=brand_name)
    category_name = brand_obj.brand_category.category_name
    context = {'category_name':category_name}
    return JsonResponse(context, safe=True)

# fetch category and brnad based on product
def get_brand_and_category(request, product_name, id=None):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    product_obj = get_object_or_404(products, product_name=product_name)
    category_name = product_obj.pro_category.category_name
    brand_name = product_obj.pro_brand.brand_name 
    context = {'product_details':[{'name':category_name, 'item':'category'},{'name':brand_name, 'item':'brand'}]}
    return JsonResponse(context, safe=True)









            
        




        
            



