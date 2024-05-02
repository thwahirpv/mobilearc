from django import template
from cart_app.models import *

register = template.Library()

@register.simple_tag(name='selling_price')
def selling_price(item):
    price = item.product.price - item.product.discount_price
    total_price = price + int(item.storage.price_of_size)
    return total_price


@register.simple_tag(name='product_sub_total')
def product_sub_total(item):
    price = item.product.price - item.product.discount_price
    total_price = price + int(item.storage.price_of_size)
    sub_tatal = total_price * item.quantity
    item.total_price = sub_tatal
    item.save()
    return sub_tatal

@register.simple_tag(name='cart_image')
def cart_image(item):
    image = item.color.images.first()
    return image.product_image.url

@register.simple_tag(name='sub_total')
def sub_total(cart_items):
    total = 0
    for item in cart_items:
        price = item.product.price - item.product.discount_price
        total_price = price + int(item.storage.price_of_size)
        total +=  item.quantity * total_price
    return total


@register.simple_tag(name='count_of_cart_items')
def count_of_cart_items(user):
    owner_obj = Owner.objects.get(customer=user)
    cart_item_count = Order.objects.filter(order_customer=owner_obj, status=0).count()
    return cart_item_count

@register.simple_tag(name='latest_two_items')
def latest_two_items(user):
    owner_obj = Owner.objects.get(customer=user)
    cart_data = Order.objects.filter(order_customer=owner_obj, status=0).order_by('-cart_id')[:2]
    return cart_data


    