# Generated by Django 5.0 on 2024-03-23 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0006_alter_userdetails_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='web_logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='logo/')),
            ],
        ),
    ]
