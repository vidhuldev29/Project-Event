# Generated by Django 4.1.5 on 2023-05-16 05:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0059_delete_convention_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convention_Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid phone number.')])),
                ('date', models.DateField()),
                ('type', models.CharField(max_length=100)),
                ('convention_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evmapp.convention')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evmapp.users')),
            ],
        ),
    ]
