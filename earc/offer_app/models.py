from django.db import models
from admin_product_app.models import category, brands, products



class category_offer(models.Model):
    offer_id = models.BigAutoField(primary_key=True, null=False, blank=False)
    discription = models.CharField(max_length=500, null=True, blank=False, unique=False)
    eligible_price = models.IntegerField(null=False, blank=False, default=0)
    discount_percentage = models.IntegerField(null=False, blank=False, default=0)
    is_active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    offer_category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='category_offer')


class brand_offer(models.Model):
    offer_id = models.BigAutoField(primary_key=True, null=False, blank=False)
    discription = models.CharField(max_length=500, null=True, blank=False, unique=False)
    eligible_price = models.IntegerField(null=False, blank=False, default=0)
    discount_percentage = models.IntegerField(null=False, blank=False, default=0)
    is_active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(brands, on_delete=models.CASCADE, related_name='brand_offer')


class product_offer(models.Model):
    offer_id = models.BigAutoField(primary_key=True, null=False, blank=False)
    discription = models.CharField(max_length=500, null=True, blank=False, unique=False)
    eligible_price = models.IntegerField(null=False, blank=False, default=0)
    discount_percentage = models.IntegerField(null=False, blank=False, default=0)
    is_active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='product_offer')
