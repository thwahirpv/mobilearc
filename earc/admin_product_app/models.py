from django.db import models

# Create your models here.

class category(models.Model):
    category_id = models.BigAutoField(primary_key=True, unique=True)
    category_name = models.CharField(max_length=50, null=False)
    category_active = models.BooleanField(default=True)
    category_disc = models.CharField(max_length=200, null=True)

class brands(models.Model):
    brand_id = models.BigAutoField(primary_key=True, unique=True)
    brand_name = models.CharField(max_length=100, null=False)
    brand_image = models.ImageField(upload_to='brands/', default='brands/brand_default_logo.png')
    brand_active = models.BooleanField(default=True)
    brand_category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='brand')

class products(models.Model):
    product_id = models.BigAutoField(primary_key=True, unique=True)
    product_name = models.CharField(max_length=50, null=False)
    product_disc = models.CharField(max_length=500, null=False)
    pro_category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='product')
    pro_brand = models.ForeignKey(brands, on_delete=models.CASCADE, related_name='pro_brand_re')
    product_active = models.BooleanField(default=True)

class variants(models.Model):
    variant_id = models.BigAutoField(primary_key=True)
    variant_color = models.CharField(max_length=100, null=False)
    variant_img = models.ImageField(upload_to='products/', default='products/user_default_image.png')
    variant_price = models.IntegerField(null=False)
    variant_product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='variations')
    
    


