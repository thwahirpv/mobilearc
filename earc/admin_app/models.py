from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from user_app.signals import pre_create


class custom_manager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        pre_create.send(sender=self.__class__, instance=user)
        user.set_password(password)
        user.save(using=self._db)
        return user



class userdetails(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, unique=True, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(_("Email Address"), unique=True, blank=False)
    phone_number = models.CharField(max_length=10, unique=True, blank=False, null=False)
    otp = models.IntegerField(unique=False, blank=True, null=True)

    objects = custom_manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
