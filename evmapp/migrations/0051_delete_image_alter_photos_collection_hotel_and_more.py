# Generated by Django 4.1.5 on 2023-05-13 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0050_image_alter_galleryimage_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AlterField(
            model_name='photos_collection',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos_collection_images', to='evmapp.accommodation'),
        ),
        migrations.AlterField(
            model_name='photos_collection',
            name='image',
            field=models.ImageField(upload_to='photos_collection'),
        ),
        migrations.AlterField(
            model_name='previousworks',
            name='image',
            field=models.ImageField(upload_to='previous_works'),
        ),
        migrations.AlterField(
            model_name='previousworks',
            name='studio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previous_works_images', to='evmapp.photography'),
        ),
    ]
