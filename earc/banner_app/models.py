from django.db import models

class priority_choices(models.IntegerChoices):
    first = 1, 'First'
    seconds = 2, 'Second'
    third = 3, 'Third'

class banner_type_choices(models.CharField):
    ('first','first_banner'),
    ('second', 'secondary_banner'),
    ('third', 'third_banner')

class Banner(models.Model):
    banner_id = models.BigAutoField(primary_key=True, unique=True)
    banner_title = models.CharField(max_length=200, null=True, blank=True)
    banner_image = models.ImageField(upload_to='banners/')
    priority = models.IntegerField(choices=priority_choices.choices, default=priority_choices.first)
    banner_text = models.CharField(max_length=500, null=True, blank=True)
    BANNER_TYPE_CHOICES = [
        ('first_banner', 'First Banner'),
        ('secondary_banner', 'Secondary Banner'),
        ('third_banner', 'Third Banner'),
    ]
    banner_type = models.CharField(choices=BANNER_TYPE_CHOICES, default='first_banner')
    banner_active = models.BooleanField(default=True)
