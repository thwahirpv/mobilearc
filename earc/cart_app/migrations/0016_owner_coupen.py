# Generated by Django 5.0 on 2024-05-03 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0015_alter_owner_owner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='coupen',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]