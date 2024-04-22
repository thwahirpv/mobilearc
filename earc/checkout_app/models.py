from django.db import models
from cart_app.models import Owner, Cart
from admin_product_app.models import products, Colors, Storage

# Create your models here.


class Order(models.Model):
    ORDER_STATUS = [
        ('processing', 'Processing'),
        ('out_of_delivery', 'Out of delivery'),
        ('delivered', 'Delivered')
    ]
    order_id = models.BigAutoField(primary_key=True, unique=True)
    order_customer = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='order_constomer')
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='order_item')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, default=None, related_name='order_color')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, default=None, related_name='order_storage')
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(null=False)
    payment_mode = models.CharField(null=False, max_length=250)
    payment_id = models.CharField(null=True)
    status = models.CharField(choices=ORDER_STATUS, default='processing')
    
