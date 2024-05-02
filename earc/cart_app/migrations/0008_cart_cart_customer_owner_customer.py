# Generated by Django 5.0 on 2024-04-17 06:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0007_remove_cart_cart_customer_remove_owner_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cart_constomer', to='cart_app.owner'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='owner',
            name='customer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to=settings.AUTH_USER_MODEL),
        ),
    ]