# Generated by Django 5.0 on 2023-12-29 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0004_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='brands',
            fields=[
                ('brand_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('brand_name', models.CharField(max_length=100)),
                ('brand_image', models.ImageField(null=True, upload_to='brands/')),
                ('brand_category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='brand', to='admin_product_app.category')),
            ],
        ),
        migrations.DeleteModel(
            name='brand',
        ),
    ]
