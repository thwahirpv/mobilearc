from django.db import models
from admin_app.models import UserDetails
from django.utils import timezone



# Create your models here.

class category(models.Model):
    category_id = models.BigAutoField(primary_key=True, unique=True)
    category_name = models.CharField(max_length=50, null=False)
    category_active = models.BooleanField(default=True)
    category_disc = models.CharField(max_length=200, null=True)
    category_image = models.ImageField(upload_to='category/', default='category/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class brands(models.Model):
    brand_id = models.BigAutoField(primary_key=True, unique=True)
    brand_name = models.CharField(max_length=100, null=False)
    brand_image = models.ImageField(upload_to='brands/', default='brands/brand_default_logo.png')
    brand_active = models.BooleanField(default=True)
    sold_out = models.IntegerField(null=True, blank=True, default=0)
    brand_category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='brands')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

class products(models.Model):
    product_id = models.BigAutoField(primary_key=True, unique=True)
    product_name = models.CharField(max_length=50, null=False)
    product_disc = models.CharField(max_length=1500, null=False)
    thumbnail = models.ImageField(upload_to='product_thumbnail/', default='product_thumbnail/default_product_thumbnail.webp')
    price = models.PositiveIntegerField(null=False)
    discount_price = models.PositiveIntegerField(null=False)
    sold_out = models.IntegerField(null=True, blank=True, default=0)
    pro_category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='product')
    pro_brand = models.ForeignKey(brands, on_delete=models.CASCADE, related_name='pro_brand_re')
    product_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def get_discount_percentage(self, size_Price):
        selling_price = self.discount_price / (self.price +  int(size_Price)) * 100
        return round(selling_price, 0)
        

class Colors(models.Model):
    color_id = models.BigAutoField(primary_key=True, unique=True)
    color_name = models.CharField(null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='colors')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    

class Images(models.Model):
    image_id = models.BigAutoField(primary_key=True, unique=True)
    product_image = models.ImageField(upload_to='products/')
    priority = models.IntegerField(null=True, blank=True)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['priority']

class Storage(models.Model):
    size_id = models.BigAutoField(primary_key=True, unique=True)
    ram = models.CharField(null=False)
    rom = models.CharField(null=False)
    price_of_size = models.CharField(null=False)
    stock = models.IntegerField(default=0)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, related_name='storage')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        ordering=['ram','rom']   


class Wishlist(models.Model):
    wishlist_id = models.BigAutoField(primary_key=True, unique=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='user')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='product')
    color = models.ForeignKey(Colors, null=True, on_delete=models.CASCADE, related_name='color', default=None)
    storage = models.ForeignKey(Storage,null=True, on_delete=models.CASCADE, related_name='storage', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)



    


