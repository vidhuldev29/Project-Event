# Generated by Django 4.1.5 on 2023-03-04 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0019_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateField()),
                ('type', models.CharField(max_length=50)),
            ],
        ),
    ]
