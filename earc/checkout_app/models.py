from django.db import models
from cart_app.models import Owner, Order
from admin_app.models import UserDetails
from admin_product_app.models import products, Colors, Storage



class review(models.Model):
    review_id = models.BigAutoField(primary_key=True, unique=True)
    comment = models.CharField(null=True)
    rate = models.IntegerField(null=False)
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='review_product')
    customer = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='review_user')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    
    



    
