# Generated by Django 4.1.5 on 2023-04-29 05:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0035_delete_decortion'),
    ]

    operations = [
        migrations.CreateModel(
            name='decortion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='')),
                ('name', models.CharField(max_length=25)),
                ('style', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid phone number.')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
