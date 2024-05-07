from django.db import models
from admin_app.models import UserDetails

# Create your models here.



class Coupen(models.Model):
    coupen_id = models.BigAutoField(primary_key=True, unique=True)
    coupen_name = models.CharField(max_length=300, null=True, blank=True)
    coupen_code = models.CharField(null=False, blank=False, unique=True)
    coupen_percentage = models.IntegerField(null=False, blank=False)
    max_amount = models.IntegerField(null=False, blank=False)
    expiration_date = models.DateTimeField(null=True)
    coupen_stock = models.IntegerField(null=False, blank=False, default=0)
    used_users = models.ManyToManyField(UserDetails, related_name='coupon_user')
    is_active = models.BooleanField(default=True)
    is_expire = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)



class User_coupon(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, unique=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='user_coupon')
    used_coupon = models.ForeignKey(Coupen, on_delete=models.CASCADE, related_name='coupon')

