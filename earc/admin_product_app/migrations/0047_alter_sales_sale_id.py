# Generated by Django 5.0 on 2024-05-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0046_sales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='sale_id',
            field=models.BigAutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
