# Generated by Django 5.0 on 2024-05-02 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0019_payment_payment_status_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='owner_id',
            field=models.BigAutoField(default=0, primary_key=True, serialize=False, unique=True),
        ),
    ]
