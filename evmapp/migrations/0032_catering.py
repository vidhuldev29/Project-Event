# Generated by Django 4.1.5 on 2023-04-28 14:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0031_galleryimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='catering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='')),
                ('name', models.CharField(max_length=25)),
                ('delivery', models.BooleanField(default=False)),
                ('service_staff', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid phone number.')])),
                ('location', models.CharField(max_length=25)),
            ],
        ),
    ]
