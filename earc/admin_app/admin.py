from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import userdetails

# Register your models here.

class customuseradmin(UserAdmin):
    model = userdetails


admin.site.register(userdetails, customuseradmin)
