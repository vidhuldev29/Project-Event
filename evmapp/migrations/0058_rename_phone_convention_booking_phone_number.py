# Generated by Django 4.1.5 on 2023-05-16 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0057_alter_convention_booking_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convention_booking',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
