# Generated by Django 5.0 on 2024-05-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0020_alter_owner_coupon_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_amount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]