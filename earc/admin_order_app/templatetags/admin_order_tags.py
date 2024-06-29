from django import template


register = template.Library()


@register.simple_tag(name='total_price')
def total_price(order_obj):
    product_price = order_obj.product.price - order_obj.product.discount_price
    product_total = product_price + int(order_obj.storage.price_of_size)
    total = order_obj.quantity * product_total 
    return total 

@register.simple_tag(name='star_percentage')
def star_percentage(item):
    return item.rate * 20


@register.simple_tag(name='shipping_charge')
def shipping_charge(order_data):
    try:
        return order_data.count() * 20
    except:
        return 20

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

