# Generated by Django 4.1.5 on 2023-05-18 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0061_transportation_booking_photography_booking_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accommodation_booking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='catering_booking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='convention_booking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='decoration_booking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='entertainment_booking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='photography_booking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='transportation_booking',
            name='user',
        ),
        migrations.DeleteModel(
            name='users',
        ),
    ]