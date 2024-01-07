from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import category, brands, products, variants
from PIL import Image
from io import BytesIO
from django.http import JsonResponse


# Category management
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

        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')

            if name == '' or discription == '':
                messages.error(request, 'Fill those fields!')
            elif not type(name) == str or not type(discription) == str:
                messages.error(request, 'Enter meaningfull details!')
            elif name.isspace() or discription.isspace():
                messages.error(request, 'Enter valid details!')
            elif len(name) < 3 or len(discription) < 5:
                messages.error(request, 'Enter valid details!')
            else:
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

# brand management
class brand_management:
    # list all brands
    def brands(request):
        categories = category.objects.all()
        brand = brands.objects.all()
        context = {'categories':categories, 'brand':brand }
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
                brands.objects.create(brand_name=name, brand_image=brand_image, brand_category=category_obj)
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

            if name == '' or category_name == '':
                messages.error(request, 'Fill those fields!')
            # Check image
            # if image:
            #     try:
            #         file_content = image.read()
            #         brand_img = Image.open(BytesIO(file_content))
            #         if not brand_img.format.lower() in ['jpeg', 'jpg', 'png']:
            #             messages.error(request, 'invalid image formate!. upload jpeg or png')
            #             return redirect('admin_products_app:update_brand')
            #     except:
            #         messages.error(request, 'Invalid file!')
            #         return redirect('admin_product_app:update_brand')
            # else:
            #     messages.error(request, 'upload image file!')
            #     return redirect('admin_product_app:update_brand')
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
    
    def delete_brand(requset, id):
        brand_obj = get_object_or_404(brands, brand_id=id)
        brand_obj.delete()
        return redirect('admin_product_app:list_brands')


# product management 
class product_management:

    def list_products(request):
        product = variants.objects.all()
        categories = category.objects.all()
        context = {'product':product, 'categories':categories}
        return render(request, 'admin_template/page-products-list.html', context)

    # add creating 
    def add_product(request):
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            product_disc = request.POST.get('product_dic')
            product_price = request.POST.get('product_price')
            product_image = request.FILES.get('product_image')
            product_color = request.POST.get('color')
            product_category = request.POST.get('product_category')
            product_brand = request.POST.get('product_brand')
            print(product_brand)

               
            # product name validatoin
            if product_name == '' or product_name.isspace() or not type(product_name) == str:
                messages.error(request, 'Enter valid name!')
                return redirect('admin_product_app:add_product')

            # product discription validation
            elif product_disc == '' or product_disc.isspace() or not type(product_disc) == str:
                messages.error(request, 'Enter valid Discription!')
                return redirect('admin_product_app:add_product')

            # product price validation 
            elif product_price == '' or product_price.isspace() or int(product_price) < 1:
                messages.error(request, 'Enter valid price!')
                return redirect('admin_product_app:add_product')

            # product color validation
            elif product_color == '' or product_color.isspace() or not type(product_color) == str:
                messages.error(request, 'Enter valid colour!')
                return redirect('admin_product_app:add_product')
            
            # product category validation
            elif product_category == 'Category':
                messages.error(request, 'select category!!')
                return redirect('admin_product_app:add_product')

            # product cateogory validation
            elif product_brand == 'Brand':
                messages.error(request, 'select Brand!')
                return redirect('admin_product_app:add_product')
            
            # Image validatoin
            if product_image:
                try:
                    file_content = product_image.read()
                    print("this is file content:", file_content)
                    image = Image.open(BytesIO(file_content))
                    if not image.format.lower() in ['jpeg', 'jpg', 'png']:
                        messages.error(request, 'invalid image formate!. upload jpeg or png')
                        return redirect(request, 'admin_product_app:add_product')
                except:
                    messages.error(request, 'Invalid file!')
                    return redirect('admin_product_app:add_product')
            else:
                messages.error(request, 'upload image!')
                return redirect('admin_product_app:add_product')    

            category_obj = get_object_or_404(category, category_name=product_category)
            brand_obj = get_object_or_404(brands, brand_name=product_brand)

            product_obj = products.objects.create(product_name=product_name, product_disc=product_disc, pro_category=category_obj, pro_brand=brand_obj)
            variants.objects.create(variant_color=product_color, variant_img=product_image, variant_price=product_price, variant_product=product_obj)
            return redirect('admin_product_app:list_products')                    


        categories = category.objects.all()
        brand = brands.objects.all()
        context = {'categories':categories, 'brand':brand}
        return render(request, 'admin_template/page-product-add.html', context)
    
    # update product
    def update_product(request, id):
        product_obj = get_object_or_404(variants, variant_id=id)
        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')
            color = request.POST.get('color')
            image = request.FILES.get('image')
            price = request.POST.get('price')

            product_obj.variant_product.product_name = name
            product_obj.variant_product.product_disc = discription
            product_obj.variant_color = color
            product_obj.variant_img = image
            product_obj.variant_price = price
            product_obj.save()
            return redirect('admin_product_app:list_products')
        context = {'product_obj':product_obj}
        return render(request, 'admin_template/update-product.html', context)

    # fetch brand based on category
    def get_brands(request, category_name):
        brand_list = []
        category_obj = get_object_or_404(category, category_name=category_name)
        brand_data = brands.objects.filter(brand_category=category_obj).values('brand_name')
        for data in brand_data:
            brand_list.append(data)
        context = {'brand_list':brand_list}
        print(context)
        return JsonResponse(context, safe=True)




            
        




        
            



