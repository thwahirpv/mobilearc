from django.db import models

# Create your models here.

class category(models.Model):
    category_id = models.BigAutoField(primary_key=True, unique=True)
    category_name = models.CharField(max_length=50, null=False)
    category_active = models.BooleanField(default=True)
    category_disc = models.CharField(max_length=200, null=True)
    category_image = models.ImageField(upload_to='category/', default='category/default.jpg')

class brands(models.Model):
    brand_id = models.BigAutoField(primary_key=True, unique=True)
    brand_name = models.CharField(max_length=100, null=False)
    brand_image = models.ImageField(upload_to='brands/', default='brands/brand_default_logo.png')
    brand_active = models.BooleanField(default=True)
    brand_category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='brands')

class products(models.Model):
    product_id = models.BigAutoField(primary_key=True, unique=True)
    product_name = models.CharField(max_length=50, null=False)
    product_disc = models.CharField(max_length=1500, null=False)
    thumbnail = models.ImageField(upload_to='product_thumbnail/', default='product_thumbnail/default_product_thumbnail.webp')
    price = models.PositiveIntegerField(null=False)
    discount_price = models.PositiveIntegerField(null=False)
    pro_category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='product')
    pro_brand = models.ForeignKey(brands, on_delete=models.CASCADE, related_name='pro_brand_re')
    product_active = models.BooleanField(default=True)

class Colors(models.Model):
    color_id = models.BigAutoField(primary_key=True, unique=True)
    color_name = models.CharField(null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='colors')
    

class Images(models.Model):
    image_id = models.BigAutoField(primary_key=True, unique=True)
    product_image = models.ImageField(upload_to='products/')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, related_name='images')

class Storage(models.Model):
    size_id = models.BigAutoField(primary_key=True, unique=True)
    ram = models.CharField(null=False)
    rom = models.CharField(null=False)
    price_of_size = models.CharField(null=False)
    stock = models.IntegerField(default=0)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, related_name='storage')
        
    class Meta:
        ordering=['ram','rom']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    
    


