# Generated by Django 5.0 on 2024-05-03 10:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_coupen_app', '0006_remove_coupen_used_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='coupen',
            name='used_users',
            field=models.ManyToManyField(related_name='coupon_user', to=settings.AUTH_USER_MODEL),
        ),
    ]