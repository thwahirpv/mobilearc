# Generated by Django 5.0 on 2024-05-04 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0022_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Cart'), (1, 'Processing'), (2, 'Shipped'), (3, 'Out of delivery'), (4, 'Delivered'), (5, 'Cancel'), (6, 'Replace'), (7, 'Return & Refund')], default=0),
        ),
    ]