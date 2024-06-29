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
    sub_tatal = item.quantity * total_price
    return sub_tatal

@register.simple_tag(name='cart_image')
def cart_image(item):
    image = item.color.images.first()
    return image.product_image.url

@register.simple_tag(name='sub_total')
def sub_total(order_data, owner_obj=None):
    total = 0
    for item in order_data:
        price = item.product.price - item.product.discount_price
        total_price = price + int(item.storage.price_of_size)
        total += total_price * item.quantity 
        total +=  item.delivery_charge
    if owner_obj is not None:   
        if owner_obj.coupon_percentage is not None:
            total = total - owner_obj.coupon_percentage/100 * total
    return total

@register.simple_tag(name='total_purchase_price')
def total_purchase_price(order_obj):
    product_total = order_obj.product.price - order_obj.product.discount_price
    product_total = product_total + int(order_obj.storage.price_of_size)
    total_price = order_obj.quantity * product_total
    return total_price

@register.simple_tag(name='percentage_star')
def percentage_star(item):
    return item.rate * 20

@register.simple_tag(name='shipping_charge')
def shipping_charge(order_data):
    return order_data.count() * 20

@register.simple_tag(name='product_price')
def product_price(order_obj):
    return order_obj.quantity * order_obj.product.price

@register.simple_tag(name='discount_price')
def discount_price(order_obj):
    return order_obj.quantity * order_obj.product.discount_price

@register.simple_tag(name='storage_price')
def storage_price(order_obj):
    return order_obj.quantity * int(order_obj.storage.price_of_size)


@register.simple_tag(name='grand_total')
def grand_total(order_obj):
    total = 0
    product_price = order_obj.product.price - order_obj.product.discount_price
    product_price += int(order_obj.storage.price_of_size)
    total = order_obj.quantity * product_price
    total = total - order_obj.coupon_amount
    total += order_obj.delivery_charge
    return total
    


# @register.simple_tag(name='bought_price')
# def bought_price(order_obj):
#     return order_obj.quantity * order_obj.product.price

# @register.simple_tag(name='discount_price')
# def discount_price(order_obj):
#     return order_obj.quantity * order_obj.product.discount_price

# @register.simple_tag(name='price_of_size')
# def price_of_size(order_obj):
#     return order_obj.quantity * order_obj.storage.price_of_size





    