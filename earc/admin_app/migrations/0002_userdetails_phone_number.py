# Generated by Django 5.0 on 2023-12-20 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='phone_number',
            field=models.CharField(default='9895779351', max_length=13, unique=True),
        ),
    ]