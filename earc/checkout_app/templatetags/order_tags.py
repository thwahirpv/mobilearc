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

@register.simple_tag(name='final_total_price')
def final_total_price(order_data, owner_obj=None):
    total = 0
    for item in order_data:
        if item.offer_object is not None: 
            discount_price = ((item.product.price + int(item.storage.price_of_size)) * item.offer_object.discount_percentage) / 100
            product_price = (item.product.price + int(item.storage.price_of_size)) - discount_price
            total_price = product_price * item.quantity
            total += total_price + item.delivery_charge
        else:
            product_price = (item.product.price + int(item.storage.price_of_size)) - item.product.discount_price
            total_price = product_price * item.quantity
            total += total_price + item.delivery_charge
    if owner_obj is not None:   
        if owner_obj.coupon_percentage is not None:
            total = total - (total * owner_obj.coupon_percentage / 100)
    return round(total, 2)


@register.simple_tag(name='sub_total')
def sub_total(order_data):
    total = 0
    for item in order_data:
        if item.offer_object is not None: 
            discount_price = ((item.product.price + int(item.storage.price_of_size)) * item.offer_object.discount_percentage) / 100
            product_price = (item.product.price + int(item.storage.price_of_size)) - discount_price
            total_price = product_price * item.quantity
            total += total_price 
        else:
            product_price = (item.product.price + int(item.storage.price_of_size)) - item.product.discount_price
            total_price = product_price * item.quantity
            total += total_price
    return round(total, 2)

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
    return (order_obj.product.price + int(order_obj.storage.price_of_size)) * order_obj.quantity

@register.simple_tag(name='total_discount_price')
def total_discount_price(order_obj):
    if order_obj.offer_object is not None:
        discount_price = ((order_obj.product.price + int(order_obj.storage.price_of_size)) * order_obj.offer_object.discount_percentage) / 100
        total_discount = discount_price * order_obj.quantity
        return total_discount
    else:
        discount_price = order_obj.product.discount_price
        total_discount = discount_price * order_obj.quantity
        return total_discount



@register.simple_tag(name='discount_price')
def discount_price(order_obj):
    if order_obj.offer_object is not None: 
        discount_price = ((order_obj.product.price + int(order_obj.storage.price_of_size)) * order_obj.offer_object.discount_percentage) / 100
        return discount_price
    else:
        discount_price = order_obj.product.discount_price
        return discount_price


@register.simple_tag(name='storage_price')
def storage_price(order_obj):
    return order_obj.quantity * int(order_obj.storage.price_of_size)


@register.simple_tag(name='grand_total')
def grand_total(order_obj):
    total = 0
    if order_obj.offer_object is not None:
        discount_price = (((order_obj.product.price + int(order_obj.storage.price_of_size)) * order_obj.offer_object.discount_percentage) / 100) * order_obj.quantity
        product_price = ((order_obj.product.price + int(order_obj.storage.price_of_size)) * order_obj.quantity) - discount_price
        total = product_price + order_obj.delivery_charge  
        if order_obj.coupon_amount is not 0:
            total -= order_obj.coupon_amount 
        return total
    else:
        discount_price = order_obj.product.discount_price * order_obj.quantity
        product_price = ((order_obj.product.price + int(order_obj.storage.price_of_size)) * order_obj.quantity) - discount_price
        total = product_price + order_obj.delivery_charge
        if order_obj.coupon_amount is not 0:
            total -= order_obj.coupon_amount 
        return total 

     
    
def item_image(item):
    image = item.color.images.first()
    return image.product_image.url

@register.simple_tag(name='product_with_storage_price')
def product_with_storage_price(order_obj):
    product_price = order_obj.product.price + int(order_obj.storage.price_of_size)
    return product_price


# @register.simple_tag(name='bought_price')
# def bought_price(order_obj):
#     return order_obj.quantity * order_obj.product.price

# @register.simple_tag(name='discount_price')
# def discount_price(order_obj):
#     return order_obj.quantity * order_obj.product.discount_price

# @register.simple_tag(name='price_of_size')
# def price_of_size(order_obj):
#     return order_obj.quantity * order_obj.storage.price_of_size





    