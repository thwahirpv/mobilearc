from django import template

register = template.Library()   

@register.simple_tag(name='total_stock_of_one_colours')
def total_stock_of_one_colours(storages):
    total = 0
    try:
        if storages:
            for item in storages:
                total += item.stock
            return total
        else:
            return 'Empty'
    except Exception as e:
        return 'Empty'
    
@register.simple_tag(name='total_product_stock')
def total_product_stock(stock_obj):
    total = 0 
    try:
        if stock_obj:
            for item in stock_obj:
                name = item.product_name
                for color_stock in item.colours:
                    for storage_stock in color_stock.storages:
                        total += storage_stock.stock
            return f'Total stock of {name}: {total}'
        else:
            return 'Empty'
    except Exception as e:
        return 'Empty'
