from django import template
from admin_app.models import web_logo
from django.templatetags.static import static


register = template.Library()

@register.simple_tag
def get_logo_url():
    try:
        logo_obj = web_logo.objects.last()
    except:
        logo_obj = None
    if logo_obj:
        return logo_obj.logo.url
    else:
        return static('assets/imgs/logo/no-logo.png')


@register.simple_tag(name='product_price')
def product_price(item):
    price = item.price - item.discount_price
    return price