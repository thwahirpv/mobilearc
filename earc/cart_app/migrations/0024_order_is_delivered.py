# Generated by Django 5.0 on 2024-05-04 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0023_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_delivered',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
