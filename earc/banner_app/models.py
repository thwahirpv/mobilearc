from django.db import models

class priority_choices(models.IntegerChoices):
    first = 1, 'First',
    seconds = 2, 'Second'
    third = 3, 'Third'

class Banner(models.Model):
    banner_id = models.BigAutoField(primary_key=True, unique=True)
    banner_title = models.CharField(max_length=200, null=True, blank=True)
    banner_image = models.ImageField(upload_to='banners/')
    priority = models.IntegerField(choices=priority_choices.choices, default=priority_choices.first)
    banner_text = models.CharField(max_length=500, null=True, blank=True)
    banner_active = models.BooleanField(default=True)
