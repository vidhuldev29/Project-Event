# Generated by Django 4.1.5 on 2023-04-19 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0024_remove_convention_website_url'),
    ]

    operations = [
        migrations.DeleteModel(
            name='convention',
        ),
    ]