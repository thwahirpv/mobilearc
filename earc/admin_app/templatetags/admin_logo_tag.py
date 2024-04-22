from django import template
from admin_app.models import web_logo


register = template.Library()

@register.simple_tag
def get_logo_url():
    logo_obj = web_logo.objects.last()
    if logo_obj:
        return logo_obj.logo.url
    return "" 
    


