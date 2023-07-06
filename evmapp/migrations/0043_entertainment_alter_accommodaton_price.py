# Generated by Django 4.1.5 on 2023-05-03 16:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0042_photos_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='entertainment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='')),
                ('name', models.CharField(max_length=25)),
                ('category', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid phone number.')])),
            ],
        ),
        migrations.AlterField(
            model_name='accommodaton',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]