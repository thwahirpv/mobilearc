# Generated by Django 5.0 on 2024-01-10 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_product_app', '0018_rename_varient_active_variants_variant_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variants',
            old_name='varient_category',
            new_name='variant_category',
        ),
    ]
