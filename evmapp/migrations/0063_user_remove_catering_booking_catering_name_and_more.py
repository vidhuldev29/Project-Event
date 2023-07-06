# Generated by Django 4.1.5 on 2023-05-18 06:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0062_remove_accommodation_booking_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=25)),
                ('username', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid phone number.')])),
                ('password', models.CharField(max_length=20)),
                ('confirmpassword', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='catering_booking',
            name='catering_name',
        ),
        migrations.RemoveField(
            model_name='convention_booking',
            name='convention_name',
        ),
        migrations.RemoveField(
            model_name='decoration_booking',
            name='decoration_name',
        ),
        migrations.RemoveField(
            model_name='entertainment_booking',
            name='program_service_name',
        ),
        migrations.RemoveField(
            model_name='photography_booking',
            name='studio_name',
        ),
        migrations.RemoveField(
            model_name='transportation_booking',
            name='travels_name',
        ),
        migrations.DeleteModel(
            name='Accommodation_Booking',
        ),
        migrations.DeleteModel(
            name='Catering_Booking',
        ),
        migrations.DeleteModel(
            name='Convention_Booking',
        ),
        migrations.DeleteModel(
            name='Decoration_Booking',
        ),
        migrations.DeleteModel(
            name='Entertainment_Booking',
        ),
        migrations.DeleteModel(
            name='Photography_Booking',
        ),
        migrations.DeleteModel(
            name='Transportation_Booking',
        ),
    ]