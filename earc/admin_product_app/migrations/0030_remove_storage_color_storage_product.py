# Generated by Django 5.0 on 2024-01-24 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0029_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='color',
        ),
        migrations.AddField(
            model_name='storage',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='storage', to='admin_product_app.colors'),
            preserve_default=False,
        ),
    ]
