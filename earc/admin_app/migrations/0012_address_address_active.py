# Generated by Django 5.0 on 2024-05-02 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0011_remove_address_address_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_active',
            field=models.BooleanField(default=True),
        ),
    ]