# Generated by Django 4.1.5 on 2023-05-13 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0048_rename_accommodaton_accommodation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(upload_to='convention_gallery'),
        ),
    ]