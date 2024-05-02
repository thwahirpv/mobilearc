# Generated by Django 5.0 on 2024-03-20 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('banner_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('banner_title', models.CharField(blank=True, max_length=200, null=True)),
                ('banner_image', models.ImageField(upload_to='banners/')),
                ('priority', models.IntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], default=1)),
                ('banner_text', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]