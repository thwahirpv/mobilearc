# Generated by Django 5.0 on 2023-12-29 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0002_category_category_disc'),
    ]

    operations = [
        migrations.AddField(
            model_name='productes',
            name='product_price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productes',
            name='pro_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product', to='admin_product_app.category'),
        ),
    ]
