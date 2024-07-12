from django.shortcuts import render, redirect
from .models import category_offer, brand_offer, product_offer
from admin_product_app.models import category, brands, products
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
import pytz
from django.urls import reverse


# =====================================Start Category offer==============================================

def list_category(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')

    offer_items = category_offer.objects.all()
    context = {
        'offer_items': offer_items
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
        except Exception as err:
            messages.warning(request, 'Enter valid eligle price or percentage')
            return redirect('admin_offer_app:add_category_offer')

        expiring = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M')
        expiring = timezone.make_aware(expiring, timezone.get_current_timezone())
        if category_offer.objects.filter(discription=discription).exists():
            messages(request, 'This offer is already exits!')
            return redirect('admin_offer_app:add_category_offer')
        elif discription is None or discription == '':
            messages.warning(request, 'Enter valid discripion')
            return redirect('admin_offer_app:add_category_offer')
        elif expiration_date is None or expiration_date == '' or expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
            messages.warning(request, 'Enter a valid time')
            return redirect('admin_offer_app:add_category_offer')
        elif eligible_price is None or eligible_price == '':
            messages.warning(request, 'Enter valid eligible price')
            return redirect('admin_offer_app:add_category_offer')
        elif discount_percentage is None or discount_percentage == '':
            messages.warning(request, 'Enter valid discount percentage')
            return redirect('admin_offer_app:add_category_offer')
        elif offer_category is None or offer_category == '':
            messages.warning(request, 'Select category')
            return redirect('admin_offer_app:add_category_offer')

        offer_category = category.objects.get(category_id=offer_category)
        try:
            category_offer.objects.create(
                discription=discription,
                eligible_price=eligible_price,
                discount_percentage=discount_percentage,
                expiration_date=expiration_date,
                offer_category=offer_category
            )
        except Exception as err:
            messages.warning(request, err)
            return redirect('admin_offer_app:add_category_offer')

        return redirect('admin_offer_app:list_category')

    items = category.objects.filter(category_active=True).all()
    context = {
        'items': items
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
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


def update_category_offer(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')

    offer_item = category_offer.objects.get(offer_id=id)
    items = category.objects.filter(category_active=True).all()
    time_of_expiring = 0
    reverse_url = reverse('admin_offer_app:update_category_offer', kwargs={'id': id})

    if request.method == 'POST':
        discription = request.POST.get('discription', offer_item.discription)
        expiration_date = request.POST.get('expiration_date', None)
        try:
            eligible_price = int(request.POST.get('eligible_price', offer_item.eligible_price))
            discount_percentage = int(request.POST.get('discount_percentage', offer_item.discount_percentage))
        except:
            messages.warning(request, 'Enter valid eligle price or percentage')
            return redirect(reverse_url)

        expiring = datetime.strptime(expiration_date if expiration_date else str(offer_item.expiration_date.strftime('%Y-%m-%dT%H:%M')), '%Y-%m-%dT%H:%M')
        expiring = timezone.make_aware(expiring, timezone.get_current_timezone())

        if category_offer.objects.exclude(discription=offer_item.discription).filter(discription=discription).exists():
            messages.warning(request, 'This offer is already exits!')
            return redirect(reverse_url)
        elif discription is None or discription == '':
            messages.warning(request, 'Enter valid discripion')
            return redirect(reverse_url)
        elif expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
            print('pass level 2 ===========')
            messages.warning(request, 'Enter a valid time')
            return redirect(reverse_url)
        elif eligible_price is None or eligible_price == '':
            messages.warning(request, 'Enter valid eligible price')
            return redirect(reverse_url)
        elif discount_percentage is None or discount_percentage == '':
            messages.warning(request, 'Enter valid discount percentage')
            return redirect(reverse_url)

        offer_item.discription = discription
        offer_item.expiration_date = expiration_date if expiration_date else offer_item.expiration_date
        offer_item.eligible_price = eligible_price
        offer_item.discount_percentage = discount_percentage
        offer_item.save()

        return redirect('admin_offer_app:list_category')

    context = {
        'offer_item': offer_item,
        'items': items
    }
    return render(request, 'admin_template/offer.html', context)


def category_offer_details(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')
    
    offer_item = category_offer.objects.get(offer_id=id)
    context = {
        'offer_item':offer_item
    }
    return render(request, 'admin_template/offer_details.html', context)


# =================================== End Category offer =============================


# =================================== Start Brand Offer =================================

def list_brand(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')

    offer_items = brand_offer.objects.all()
    context = {
        'offer_items': offer_items
    }
    return render(request, 'admin_template/offer_list.html', context)


def add_brand_offer(request):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')

    if request.method == 'POST':
        discription = request.POST.get('discription', None)
        expiration_date = request.POST.get('expiration_date', None)
        brand = request.POST.get('brand', None)
        try:
            discount_percentage = int(request.POST.get('discount_percentage', None))
            eligible_price = int(request.POST.get('eligible_price', None))
        except Exception as err:
            print('this is error')
            print(err)
            messages.warning(request, err)
            return redirect('admin_offer_app:add_brand_offer')

        expiring = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M')
        expiring = timezone.make_aware(expiring, timezone.get_current_timezone())
        

        if brand_offer.objects.filter(discription=discription).exists():
            messages(request, 'This offer is already exits!')
        elif discription == None or discription == '':
            messages.warning(request, 'Enter valid discription!')
            return redirect('admin_offer_app:add_brand_offer')
        elif expiration_date == None or expiration_date == '' or expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
            messages.warning(request, 'Select valid time!')
            return redirect('admin_offer_app:add_brand_offer')
        elif brand == None or brand == '':
            messages.warning(request, 'Select a Brand')
            return redirect('admin_offer_app:add_brand_offer')
        elif discount_percentage == None or discount_percentage == '':
            messages.warning(request, 'Enter a valid percentage')
            return redirect('admin_offer_app:add_brand_offer')
        elif eligible_price == None or eligible_price == '':
            messages.warning(request, 'Enter valid eligible price!')
            return redirect('admin_offer_app:add_brand_offer')

        offer_brand = brands.objects.get(brand_id=brand)

        try:
            brand_offer.objects.create(
                discription=discription,
                eligible_price=eligible_price,
                discount_percentage=discount_percentage,
                expiration_date=expiration_date,
                brand=offer_brand
            )
        except Exception as err:
            messages.warning(request, err)
            return redirect('admin_offer_app:add_brand_offer')

        return redirect('admin_offer_app:list_brand')

    items = brands.objects.filter(brand_active=True).all()
    context = {
        'items': items
    }
    return render(request, 'admin_template/offer.html', context)


def update_brand_offer(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')

    offer_item = brand_offer.objects.get(offer_id=id)
    items = brands.objects.filter(brand_active=True).all()
    reverse_url = reverse('admin_offer_app:update_brand_offer', kwargs={'id':id})
    expiring = 0

    if request.method == 'POST':
        discription = request.POST.get('discription', None)
        expiration_date = request.POST.get('expiration_date', None)
        brand = request.POST.get('brand', None)
        try:
            discount_percentage = int(request.POST.get('discount_percentage', None))
            eligible_price = int(request.POST.get('eligible_price', None))
        except:
            messages.warning(request, 'Enter valid eligle price or percentage')
            return redirect(reverse_url)

        expiring = datetime.strptime(expiration_date if expiration_date else str(offer_item.expiration_date.strftime('%Y-%m-%dT%H:%M')), '%Y-%m-%dT%H:%M')
        expiring = timezone.make_aware(expiring, timezone.get_current_timezone())


        if brand_offer.objects.exclude(discription=offer_item.discription).filter(discription=discription).exists():
            messages.warning(request, 'This offer is already exits!')
            return redirect(reverse_url) 
        elif discription == None or discription == '':
            messages.warning(request, 'Enter valid discription!')
            return redirect(reverse_url)
        elif expiring < datetime.utcnow().replace(tzinfo=pytz.utc):
            messages.warning(request, 'Enter valid time!')
            return redirect(reverse_url)
        elif discount_percentage == None or discount_percentage == '':
            messages.warning(request, 'Enter a valid percentage')
            return redirect(reverse_url)
        elif eligible_price == None or eligible_price == '':
            messages.warning(request, 'Enter valid eligible price!')
            return redirect(reverse_url)

        try:
            offer_item.discription = discription
            offer_item.expiration_date = expiration_date if expiration_date else offer_item.expiration_date
            offer_item.discount_percentage = discount_percentage
            offer_item.eligible_price = eligible_price
            offer_item.save()
        except Exception as err:
            messages.warning(request, err)
            return redirect(reverse_url)

        return redirect('admin_offer_app:list_brand')

    context = {
        'items': items,
        'offer_item': offer_item
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


def brand_details(request, id):
    if not request.user.is_authenticated or request.user.is_superuser is False:
        return redirect('admin_app:admin_login')
    
    offer_item = brand_offer.objects.get(offer_id=id)
    context = {
        'offer_item':offer_item
    }
    return render(request, 'admin_template/offer_details.html', context)


# ====================================== End Brand offer =======================
