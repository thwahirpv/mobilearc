from django.shortcuts import render
from admin_app.models import Address


# Create your views here.


def checkout(request):
    user = request.user
    address_data = Address.objects.filter(user=user)
    
    context = {
        'address_data':address_data,
    }
    return render(request, 'user_template/shop-checkout.html', context)
