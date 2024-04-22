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
        total += total_price * item.quantity
    return total
    