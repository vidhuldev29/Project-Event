# Generated by Django 4.1.5 on 2023-05-31 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0069_transportationbooking_photographybooking_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galleryimage',
            name='convention',
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='convention',
            field=models.ManyToManyField(related_name='gallery_images', to='evmapp.convention'),
        ),
    ]
