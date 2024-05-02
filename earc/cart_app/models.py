from django.db import models
from admin_app.models import UserDetails, Address
from admin_product_app.models import *

# Create your models here.




class Owner(models.Model):
    owner_id = models.BigAutoField(primary_key=True, unique=True, default=0)
    customer = models.OneToOneField(UserDetails, on_delete=models.SET_NULL, null=True, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    payment_id = models.CharField(null=True, default=0)
    payment_mode = models.CharField(max_length=200, default='COD')
    payment_status = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    ORDER_STATUS = [
        (0, 'Cart'),
        (1, 'Processing'),
        (2, 'Shipped'),
        (3, 'Out of delivery'),
        (4, 'Delivered'),
        (5, 'Cancel')
    ]
    cart_id = models.BigAutoField(primary_key=True, unique=True)
    # order_customer = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='order_costm')
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='order_item')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, default=None, related_name='order_color')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, default=None, related_name='order_storage')
    quantity = models.IntegerField(default=1)
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    # order_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, related_name='ordered_address', default=None)
    # order_payment = models.OneToOneField(Payment, on_delete=models.DO_NOTHING, null=True, related_name='order_payment', default=None)
    total_price = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


