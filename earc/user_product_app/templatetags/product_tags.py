from django import template 

register = template.Library()

@register.simple_tag(name='star_percentage')
def star_percentage(item):
    return item.rate * 20