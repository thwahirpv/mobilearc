from django import template 
from user_product_app.views import set_product_price

register = template.Library()

@register.simple_tag(name='star_percentage')
def star_percentage(item):
    return item.rate * 20

@register.simple_tag(name='product_price')
def product_price(product_obj, size_of_price):
    price = set_product_price(product_obj, int(size_of_price))['total_price']
    return price