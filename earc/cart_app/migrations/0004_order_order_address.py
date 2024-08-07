# Generated by Django 5.0 on 2024-05-02 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0012_address_address_active'),
        ('cart_app', '0003_remove_order_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_address',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ordered_address', to='admin_app.address'),
        ),
    ]
