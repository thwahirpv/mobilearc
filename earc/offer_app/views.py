from django.shortcuts import render, redirect
from .models import category_offer, brand_offer, product_offer
from admin_product_app.models import category, brands, products
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
import pytz


# =====================================Start Category offer==============================================

def list_category(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    offer_items = category_offer.objects.all()
    context = {
        'offer_items':offer_items
    }
    return render(request, 'admin_template/offer_list.html', context)


def add_category_offer(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    
    if request.method == 'POST':
        discription = request.POST.get('discription', None)
        expiration_date = request.POST.get('expiration_date', None)
        offer_category = request.POST.get('offer_category', None)
        try:
            eligible_price = int(request.POST.get('eligible_price', None))
            discount_percentage = int(request.POST.get('discount_percentage', None))
        except:
            messages.warning(request, 'Enter valid eligle price or percentage')
        
        expiring = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M')
        expiring= timezone.make_aware(expiring, timezone.get_current_timezone())

        if discription is None or discription == '':
            messages.warning(request, 'Enter valid discripion')
        elif expiration_date is None or expiration_date == '' or expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
             messages.warning(request, 'Enter a valid time') 
        elif eligible_price is None or eligible_price == '':
             messages.warning(request, 'Enter valid eligible price')
        elif discount_percentage is None or discount_percentage == '':
             messages.warning(request, 'Enter valid discount percentage')
        elif offer_category is None or offer_category == '':
             messages.warning(request, 'Select category')

        offer_category = category.objects.get(category_id=offer_category)
        try:
            category_offer.objects.create(
                discription=discription,
                eligible_price=eligible_price,
                discount_percentage=discount_percentage,
                expiration_date=expiration_date,
                offer_category = offer_category
            )
        except Exception as err:
             messages.warning(request, err)
        
        return redirect('admin_offer_app:list_category')

    items = category.objects.filter(category_active=True).all()
    context = {
         'items':items
    }
    return render(request, 'admin_template/offer.html', context)

def block_unblock_category(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')
    try:
        item = category_offer.objects.get(offer_id=id)
        if item.is_active is True:
            item.is_active = False
            item.save()
        else:
             item.is_active = True
             item.save()
    except:
        pass
    return redirect('admin_offer_app:list_category')


def update_category_offer(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')
    
    offer_item = category_offer.objects.get(offer_id=id)
    items = category.objects.filter(category_active=True).all()
    expiring = 0

    if request.method == 'POST':
        discription = request.POST.get('discription', offer_item.discription)
        expiration_date = request.POST.get('expiration_date', None)
        offer_category = request.POST.get('offer_category', offer_item.offer_category)
        try:
            eligible_price = int(request.POST.get('eligible_price', offer_item.eligible_price))
            discount_percentage = int(request.POST.get('discount_percentage', offer_item.discount_percentage))
        except:
            messages.warning(request, 'Enter valid eligle price or percentage')
        if expiration_date:
            expiring = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M')
            expiring= timezone.make_aware(expiring, timezone.get_current_timezone())

        if discription is None or discription == '':
            messages.warning(request, 'Enter valid discripion')
        elif expiration_date is None or expiration_date == '' or expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
             messages.warning(request, 'Enter a valid time') 
        elif eligible_price is None or eligible_price == '':
             messages.warning(request, 'Enter valid eligible price')
        elif discount_percentage is None or discount_percentage == '':
             messages.warning(request, 'Enter valid discount percentage')
        elif offer_category is None or offer_category == '':
             messages.warning(request, 'Select category')

        offer_category = category.objects.get(category_id=offer_category)
        offer_item.discription = discription
        offer_item.expiration_date = expiration_date if expiration_date else offer_item.expiration_date
        offer_item.eligible_price = eligible_price
        offer_item.discount_percentage = discount_percentage
        offer_item.offer_category = offer_category
        offer_item.save()

        return redirect('admin_offer_app:list_category')

    context = {
        'offer_item':offer_item,
        'items':items
    }
    return render(request, 'admin_template/offer.html', context)

# =================================== End Category offer =============================


# =================================== Start Brand Offer =================================

def list_brand(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
            return redirect('admin_app:admin_login')
    

def add_brand_offer(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')
    
    if request.method == 'POST':
        discription = request.POST.get('discription', None)
        expiration_date = request.POST.get('expiration_date', None)
        brand = request.POST.get('brand', None)
        try:
            discount_percentage = int(request.POST.get('discount_percentage',None))
            eligible_price = int(request.POST.get('eligible_price'), None)
        except:
            messages.warning(request, 'Enter valid eligle price or percentage')

        
        expiring = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M')
        expiring= timezone.make_aware(expiring, timezone.get_current_timezone())

        if discription == None or discription == '':
            messages.warning(request, 'Enter valid discription!')
        elif expiration_date == None or expiration_date == '' or expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
             messages.warning(request, 'Offer Expired!')
        elif brand == None or brand == '':
             messages.warning(request, 'Select a Brand')
        elif discount_percentage == None or discount_percentage == '':
             messages.warning(request, 'Enter a valid percentage')
        elif eligible_price == None or eligible_price == '':
             messages.warning(request, 'Enter valid eligible price!')

        offer_brand = brands.objects.get(brand_id=brand)

        try:
            brand_offer.objects.create(
                discription = discription,
                eligible_price = eligible_price,
                discount_percentage = discount_percentage,
                expiration_date = expiration_date,
                brand = offer_brand
            )
        except Exception as err:
            messages.warning(request, err)

        return redirect('admin_offer_app:list_brand')
    
    items = brands.objects.filter(brand_active=True).all()
    context = {
        'items':items
    }
    return render(request, 'admin_template/offer.html', context)


def update_brand_offer(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')
    
    offer_item = brand_offer.objects.get(offer_id=id)
    items = brands.objects.filter(brand_active=True).all()
    expirig = 0
    
    if request.method == 'POST':
        discription = request.POST.get('discription', None)
        expiration_date = request.POST.get('expiration_date', None)
        brand = request.POST.get('brand', None)
        try:
            discount_percentage = int(request.POST.get('discount_percentage',None))
            eligible_price = int(request.POST.get('eligible_price'), None)
        except:
            messages.warning(request, 'Enter valid eligle price or percentage')

        if expiration_date:
            expiring = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M')
            expiring= timezone.make_aware(expiring, timezone.get_current_timezone())


        if discription == None or discription == '':
            messages.warning(request, 'Enter valid discription!')
        elif expiration_date == None or expiration_date == '' or expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
             messages.warning(request, 'Offer Expired!')
        elif brand == None or brand == '':
             messages.warning(request, 'Select a Brand')
        elif discount_percentage == None or discount_percentage == '':
             messages.warning(request, 'Enter a valid percentage')
        elif eligible_price == None or eligible_price == '':
             messages.warning(request, 'Enter valid eligible price!')

        try:
            offer_item.discription = discription
            offer_item.expiration_date = expiration_date
            offer_item.brand = brand
            offer_item.discount_percentage = discount_percentage
            offer_item.eligible_price = eligible_price
        except Exception as err:
             messages.warning(request, err) 
        
        return redirect('admin_offer_app:list_brand')
    
    context = {
        'items':items
    }
    return render(request, 'admin_template/offer.html', context)


def block_and_unblock_brand(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')
    
    try:
        offer_brand = brand_offer.objects.get(offer_id=id)
    except Exception as err:
        pass
    
    if offer_brand.is_active is True:
         offer_brand.is_active = False
         offer_brand.save()
    else:
         offer_brand.is_active = True
         offer_brand.save()
    return redirect('admin_offer_app:list_brand')
     
# ====================================== End Brand offer =======================
    





    
        
     
     
     
