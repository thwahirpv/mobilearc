from django.http import JsonResponse
from django.shortcuts import redirect, render
from admin_product_app.models import category, brands, products, variants


def product_list(request):
    products_data = products.objects.all()
    category_data = category.objects.all()
    choosed_category = request.GET.get('x', None)
    if choosed_category is not None:
        products_data = products.objects.filter(pro_category__category_name=choosed_category)
    context={'products_data':products_data, 'category_data':category_data}
    return render(request, 'user_template/list_products.html', context)
