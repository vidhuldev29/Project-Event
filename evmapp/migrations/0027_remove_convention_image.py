# Generated by Django 4.1.5 on 2023-04-19 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0026_convention'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='image',
        ),
    ]
