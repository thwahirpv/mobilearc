from django import template
from cart_app.models import *

register = template.Library()

@register.simple_tag(name='selling_price')
def selling_price(item):
    if item.offer_object is not None:
        discount_price = ((item.product.price + int(item.storage.price_of_size)) * item.offer_object.discount_percentage) / 100
        product_price = (item.product.price + int(item.storage.price_of_size)) - discount_price
        item.total_price = product_price
        item.save()
        return round(product_price)
    else:
        product_price = (item.product.price + int(item.storage.price_of_size)) - item.product.discount_price
        item.total_price = product_price
        item.save()
        return round(product_price)


@register.simple_tag(name='product_sub_total')
def product_sub_total(item):
    if item.offer_object is not None:
        discount_price = ((item.product.price + int(item.storage.price_of_size)) * item.offer_object.discount_percentage) / 100
        product_price = (item.product.price + int(item.storage.price_of_size)) - discount_price
        total_price = product_price * item.quantity
        item.total_price = total_price
        item.save()
        return round(total_price)
    else:
        product_price = (item.product.price + int(item.storage.price_of_size)) - item.product.discount_price
        total_price = product_price * item.quantity
        item.total_price = total_price
        item.save()
        return round(total_price)

    

@register.simple_tag(name='cart_image')
def cart_image(item):
    image = item.color.images.first()
    return image.product_image.url

@register.simple_tag(name='sub_total')
def sub_total(cart_items):
    total = 0
    for item in cart_items:
        if item.offer_object is not None: 
            discount_price = ((item.product.price + int(item.storage.price_of_size)) * item.offer_object.discount_percentage) / 100
            product_price = (item.product.price + int(item.storage.price_of_size)) - discount_price
            total_price = product_price * item.quantity
            total += total_price
        else:
            product_price = (item.product.price + int(item.storage.price_of_size)) - item.product.discount_price
            total_price = product_price * item.quantity
            total += total_price
    return round(total)


@register.simple_tag(name='count_of_cart_items')
def count_of_cart_items(user):
    owner_obj = Owner.objects.get(customer=user)
    cart_item_count = Order.objects.filter(order_customer=owner_obj, status=0).count()
    return cart_item_count

@register.simple_tag(name='latest_two_items')
def latest_two_items(user):
    cart_data = None
    try:
        owner_obj = Owner.objects.get(customer=user)
    except:
        owner_obj = Owner.objects.none()
    if owner_obj:
        try:
            cart_data = Order.objects.filter(order_customer=owner_obj, status=0).order_by('-created_at')[:2]
        except:
            cart_data = Order.objects.none()
    return cart_data