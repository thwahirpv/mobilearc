# Generated by Django 5.0 on 2024-04-17 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0004_alter_cart_cart_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='customer',
        ),
    ]
