from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import category, brands, products, variants


# Category management
class category_management:
    # category lising and add new category
    def category(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')
            if name is None or discription is None:
                messages.error(request, 'Fill those fields!')
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
            elif category.objects.filter(category_name=name).exists():
                messages.error(request, f'{name} is already exist')
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
            category_obj.category_active = False
            category_obj.save()
            return redirect('admin_product_app:admin_category')
        elif action == 'unblock':
            category_obj.category_active = True
            category_obj.save()
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
            print(category_name)
            if name == '' or category_name == '':
                messages.error(request, 'Fill name and category!')
                return redirect('admin_product_app:add_brand')
            elif brands.objects.filter(brand_name=name).exists():
                messages.error(request, f'{name} is already exits')
                return redirect('admin_product_app:add_brand')
            else:
                category_obj = get_object_or_404(category, category_name=category_name)
                brands.objects.create(brand_name=name, brand_image=brand_image, brand_category=category_obj)
                return redirect('admin_product_app:list_brands')
        categories = category.objects.all()
        return render(request, 'admin_template/page-addbrand.html', {'categories':categories})


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

            category_obj = get_object_or_404(category, category_name=product_category)
            brand_obj = get_object_or_404(brands, brand_name=product_brand)

            product_obj = products.objects.create(product_name=product_name, product_disc=product_disc, pro_category=category_obj, pro_brand=brand_obj)
            variants.objects.create(variant_color=product_color, variant_img=product_image, variant_price=product_price, variant_product=product_obj)
            return redirect('admin_product_app:list_products')                    


        categories = category.objects.all()
        brand = brands.objects.all()
        context = {'categories':categories, 'brand':brand}
        return render(request, 'admin_template/page-product-add.html', context)
    
    def update_product(request, id):
        product_obj = get_object_or_404(products, product_id=id)
        variants_obj = get_object_or_404(variants, variant_product=product_obj)
        if request.method == 'POST':
            name = request.POST.get('name')
            discription = request.POST.get('discription')
            color = request.POST.get('color')
            image = request.POST.get('image')
            price = request.POST.get('price')

            product_obj.product_name = name
            product_obj.product_disc = discription
            product_obj.save()
            variants_obj.variant_color = color
            variants_obj.variant_img = image
            variants_obj.variant_price = price
            variants_obj.save()
            return redirect('admin_product_app:list_products')
        context = {'product_obj':product_obj, 'variants_obj':variants_obj}
        return render(request, 'admin_template/page-update-product.html', context)


            
        




        
            



