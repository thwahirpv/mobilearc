# Generated by Django 5.0 on 2024-01-22 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0022_products_discount_price_products_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='price_of_size',
            field=models.CharField(default=1),
            preserve_default=False,
        ),
    ]
