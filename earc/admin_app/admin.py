from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import UserDetails




# Register your models here.

class customuseradmin(UserAdmin):
    fieldsets=(
        (None, {'fields':('email','phone_number','password')}), 
        (_('Personal info'), {'fields':('first_name','last_name')}),
        (_('Permissions'), {'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        (_('Important dates'), {'fields':('date_joined','last_login')}),
    )
    add_fieldsets=(
        (None, {
            'classes':('wide',),
            'fields':('username','email','phone_number','password','password2'),
        }),
    )
    list_display=('username','email','phone_number','is_active')
    search_fields=('username','email','phone_number')
    ordering=('user_id',)


admin.site.register(get_user_model(), customuseradmin)
