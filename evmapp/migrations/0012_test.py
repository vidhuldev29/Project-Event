# Generated by Django 4.1.5 on 2023-02-24 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0011_delete_aud1book_delete_venuemile'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('type', models.CharField(max_length=50)),
            ],
        ),
    ]
