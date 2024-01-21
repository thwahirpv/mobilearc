from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import category, brands, products
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
# ==================================================================================================================


#=========================================== start Category management ====================================================
class category_management:
    # category lising and add new category
    def category(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')
            if name == '' or discription == '':
                messages.error(request, 'Fill those fields!')
                return redirect('admin_product_app:admin_category')
            elif not type(name) == str and type(discription) == str:
                messages.error(request, 'Enter meaningfull details!')
                return redirect('admin_product_app:admin_category')
            elif name.isspace() or discription.isspace():
                messages.error(request, 'Enter valid details!')
                return redirect('admin_product_app:admin_category')
            elif len(name) < 3 or len(discription) < 5:
                messages.error(request, 'Enter valid details!')
                return redirect('admin_product_app:admin_category')
            elif category.objects.filter(category_name=name).exists():
                messages.error(request, f'{name} is already exist')
                return redirect('admin_product_app:admin_category')
            else:
                category.objects.create(category_name=name, category_disc=discription)
                return redirect('admin_product_app:admin_category')
        categories = category.objects.all()
        context = {'cotegories':categories}
        return render(request, 'admin_template/page-categories.html', context)
    
    # category delete
    def delete_category(requset, id):
        category_obj = get_object_or_404(category, category_id=id)
        category_obj.delete()
        return redirect('admin_product_app:admin_category')
    
    # category update
    def update_category(request, id):
        category_obj = get_object_or_404(category, category_id=id)
        reverse_url = reverse('admin_product_app:update_category', kwargs={'id':id})

        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')

            if name == '' or discription == '':
                messages.error(request, 'Fill those fields!')
                return redirect(reverse_url)
            elif not type(name) == str or not type(discription) == str:
                messages.error(request, 'Enter meaningfull details!')
                return redirect(reverse_url)
            elif name.isspace() or discription.isspace():
                messages.error(request, 'Enter valid details!')
                return redirect(reverse_url)
            elif len(name) < 3 or len(discription) < 5:
                messages.error(request, 'Enter valid details!')
                return redirect(reverse_url)
            elif not name == category_obj.category_name:
                if category.objects.filter(category_name=name).exists():
                    messages.error(request, f'{name} is already exists!')
                    return redirect(reverse_url)
            
            category_obj.category_name = name
            category_obj.category_disc = discription
            category_obj.save()               
            return redirect('admin_product_app:admin_category')
        return render(request, 'admin_template/page-update-category.html', {'category_obj':category_obj})
    
    # category block and unblock
    def block_and_unblock(requset, action, id):
        category_obj = get_object_or_404(category, category_id=id)
        if action == 'block':
            category.objects.filter(category_id=id).update(category_active=False)
            brands.objects.filter(brand_category=category_obj).update(brand_active=False)
            products.objects.filter(pro_category=category_obj).update(product_active=False)
            return redirect('admin_product_app:admin_category')
        elif action == 'unblock':
            category.objects.filter(category_id=id).update(category_active=True)
            brands.objects.filter(brand_category=category_obj).update(brand_active=True)
            products.objects.filter(pro_category=category_obj).update(product_active=True)
            return redirect('admin_product_app:admin_category')
#=========================================== end Category management ====================================================



#=========================================== start brand management ====================================================    
# brand management
class brand_management:
    # list all brands
    def brands(request):
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
    def add_brand(request):
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
    def update_brand(request, id):
        categories = category.objects.all()
        brand = get_object_or_404(brands, brand_id=id)
        if request.method == 'POST':
            name = request.POST.get('name')
            image = request.FILES.get('brand_image')
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
                messages.error(request, 'upload image file!')
                return redirect('admin_product_app:update_brand')

            if name == '' or category_name == '':
                messages.error(request, 'Fill those fields!')

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
    def block_and_unblock(requset, action, id):
        brand_obj = get_object_or_404(brands, brand_id=id)
        if action == 'block':
            brands.objects.filter(brand_id=id).update(brand_active=False)
            products.objects.filter(pro_brand=brand_obj).update(product_active=False)
            return redirect('admin_product_app:list_brands')
        elif action == 'unblock':
            brands.objects.filter(brand_id=id).update(brand_active=True)
            products.objects.filter(pro_brand=brand_obj).update(product_active=True)
            return redirect('admin_product_app:list_brands')

    # delete brand
    def delete_brand(requset, id):
        brand_obj = get_object_or_404(brands, brand_id=id)
        brand_obj.delete()
        return redirect('admin_product_app:list_brands')
#=========================================== end brand management ====================================================



#=========================================== start product management ================================================  
# product management 
class product_management:
    # show all prosucts 
    def list_products(request):
        name = request.GET.get('brand', None)
        status = request.GET.get('status', None)
        product_data = products.objects.all()
        status_data = 'All'
        brand_name = 'All Brands'

        # Filter Active and Blocked products
        if status is not None:
            if 'All' in status:
                pass
            elif 'Active' in status:
                product_data = products.objects.filter(product_active=True)
                status_data = 'Active'
            elif 'Blocked' in status:
                product_data = products.objects.filter(product_active=False)
                status_data = 'Blocked'
        # Filter brand base products
        else:
            if name is None:
                pass
            elif 'all' in name:
                brand_name = 'All Brands'
            elif name is not None:
                product_data = products.objects.filter(pro_brand__brand_name=name)
                brand_name = name
        brands_data = brands.objects.all()
        context = {'product_data':product_data, 'brands_data':brands_data, 'brand_name':brand_name, 'status_data':status_data}
        return render(request, 'admin_template/page-products-list.html', context)

    # add new product  
    def add_product(request):
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            product_disc = request.POST.get('product_dic')
            product_category = request.POST.get('product_category')
            product_brand = request.POST.get('product_brand')
            product_image = request.FILES.get('product_image')

            if product_image:
                try:
                    file_content = product_image.read()
                    image = Image.open(BytesIO(file_content))
                    print(image.format.lower)
                    if not image.format.lower() in ['jpeg', 'jpg', 'png']:
                        messages.error(request, 'invalid image formate!. upload jpeg or png')
                        return redirect('admin_product_app:add_product')
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect('admin_product_app:add_product')
            else:
                messages.error(request, 'upload image!')
                return redirect('admin_product_app:add_product')
            # product name validatoin
            if product_name == '' or product_name.isspace() or not type(product_name) == str:
                messages.error(request, 'Enter valid name!')
                return redirect('admin_product_app:add_product')

            # product discription validation
            elif product_disc == '' or product_disc.isspace() or not type(product_disc) == str:
                messages.error(request, 'Enter valid Discription!')
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
            elif products.objects.filter(product_name=product_name).exists():
                messages.error(request, f'{product_name} is alreay exists')
                return redirect('admin_product_app:add_product')

            category_obj = get_object_or_404(category, category_name=product_category)
            brand_obj = get_object_or_404(brands, brand_name=product_brand)
            product_obj = products.objects.create(product_name=product_name, product_disc=product_category, product_image=product_image, pro_category=category_obj, pro_brand=brand_obj) 
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
        product_obj = get_object_or_404(products, product_id=id)
        brands_data = brands.objects.all()
        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')
            product_image = request.FILES.get('image')
            pro_category = request.POST.get('category')
            pro_brand = request.POST.get('brand')

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
            product_obj.product_image = product_image
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
        product_obj = get_object_or_404(products, product_id=id)
        if action == 'block':
            product_obj.product_active = False
            product_obj.save()
            return redirect('admin_product_app:list_products')
        elif action == 'unblock':
            product_obj.product_active = True
            product_obj.save()
            return redirect('admin_product_app:list_products')
#=========================================== end product management ====================================================


   



# fetch brand based on category
def get_category(request, brand_name, id=None):
    brand_obj = get_object_or_404(brands, brand_name=brand_name)
    category_name = brand_obj.brand_category.category_name
    context = {'category_name':category_name}
    return JsonResponse(context, safe=True)

# fetch category and brnad based on product
def get_brand_and_category(request, product_name, id=None):
    product_obj = get_object_or_404(products, product_name=product_name)
    category_name = product_obj.pro_category.category_name
    brand_name = product_obj.pro_brand.brand_name 
    context = {'product_details':[{'name':category_name, 'item':'category'},{'name':brand_name, 'item':'brand'}]}
    return JsonResponse(context, safe=True)
    




            
        




        
            



