# Generated by Django 5.0 on 2024-01-24 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0024_alter_size_options_alter_size_ram_alter_size_rom'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Size',
        ),
    ]
