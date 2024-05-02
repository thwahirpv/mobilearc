from django import template


register = template.Library()

@register.simple_tag(name='unit_price')
def unit_price(order_obj):
    total_price = order_obj.product.price - order_obj.product.discount_price
    total = total_price + int(order_obj.storage.price_of_size)
    return total

@register.simple_tag(name='total_price')
def total_price(order_obj):
    product_price = order_obj.product.price - order_obj.product.discount_price
    product_total = product_price + int(order_obj.storage.price_of_size)
    total = order_obj.quantity * product_total 
    return total 

@register.simple_tag(name='star_percentage')
def star_percentage(item):
    return item.rate * 20

