from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from user_app import signals


class custom_manager(BaseUserManager):
    def _create_user(self, email, phone_number, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        signals.pre_create.send(sender=self.__class__, instance=user)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Sulperuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
        



class UserDetails(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, unique=True, blank=False)
    username = models.CharField(max_length=30, blank=False)
    email = models.EmailField(_("Email Address"), unique=True, blank=False)
    phone_number = models.CharField(max_length=10, unique=True, blank=False)
    verification_status = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = custom_manager()

    def __str__(self):
        return self.email
