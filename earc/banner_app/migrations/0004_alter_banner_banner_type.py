# Generated by Django 5.0 on 2024-03-25 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner_app', '0003_banner_banner_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_type',
            field=models.CharField(choices=[('first', 'First Banner'), ('second', 'Secondary Banner'), ('third', 'Third Banner')], default=('first', 'First Banner')),
        ),
    ]