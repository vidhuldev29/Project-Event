# Generated by Django 4.1.5 on 2023-05-16 04:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0056_convention_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention_booking',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid phone number.')]),
        ),
    ]