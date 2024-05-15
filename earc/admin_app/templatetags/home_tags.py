from django import template
from cart_app.models import Order
from admin_product_app.models import category, products
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear

register = template.Library()

@register.simple_tag(name='total_revenue')
def total_revenue():
    total = 0
    try:
        order_data = Order.objects.filter(status=4)
    except:
        order_data = Order.objects.none()

    if order_data:
        for item in order_data:
            total += item.total_price
        return total
    else:
        return 0

@register.simple_tag(name='total_order')
def total_order():
    order_count = Order.objects.filter(status__gt=0, status__lt=5,)
    return order_count.count()


@register.simple_tag(name='category_count')
def category_count():
    categories = category.objects.all()
    return categories.count()

@register.simple_tag(name='product_count')
def product_count():
    all_products = products.objects.all()
    return all_products.count()
    
