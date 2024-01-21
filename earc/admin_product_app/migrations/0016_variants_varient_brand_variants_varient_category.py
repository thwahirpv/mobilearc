# Generated by Django 5.0 on 2024-01-08 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0015_variants_varient_disc'),
    ]

    operations = [
        migrations.AddField(
            model_name='variants',
            name='varient_brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='varient_brand_re', to='admin_product_app.brands'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variants',
            name='varient_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='varient_category_re', to='admin_product_app.category'),
            preserve_default=False,
        ),
    ]
