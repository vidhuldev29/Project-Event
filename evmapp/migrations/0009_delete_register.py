# Generated by Django 4.1.5 on 2023-02-15 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0008_users_alter_register_phone'),
    ]

    operations = [
        migrations.DeleteModel(
            name='register',
        ),
    ]