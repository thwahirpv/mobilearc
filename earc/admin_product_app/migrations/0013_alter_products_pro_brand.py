# Generated by Django 5.0 on 2024-01-06 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0012_alter_brands_brand_category_alter_products_pro_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='pro_brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro_brand_re', to='admin_product_app.brands'),
        ),
    ]
