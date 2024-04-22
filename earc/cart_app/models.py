from django.db import models
from admin_app.models import UserDetails
from admin_product_app.models import *

# Create your models here.


class Owner(models.Model):
    class ItemStage(models.IntegerChoices):
        cart = 0, 'cart'
        order = 1, 'order'
    
    owner_id = models.BigAutoField(primary_key=True, unique=True)
    customer = models.OneToOneField(UserDetails, on_delete=models.SET_NULL, null=True, related_name='order')
    stage = models.IntegerField(choices=ItemStage.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    cart_id = models.BigAutoField(primary_key=True, unique=True)
    cart_customer = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='cart_constomer')
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='cartitem')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, default=None, related_name='cartcolor')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, default=None, related_name='cartstorage')
    quantity = models.IntegerField(default=1)
