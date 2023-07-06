# Generated by Django 4.1.5 on 2023-04-18 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0022_delete_convention'),
    ]

    operations = [
        migrations.CreateModel(
            name='convention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='')),
                ('name', models.CharField(max_length=25)),
                ('seating', models.IntegerField()),
                ('dining', models.IntegerField()),
                ('parking', models.IntegerField()),
                ('price', models.IntegerField()),
                ('place', models.CharField(max_length=25)),
                ('district', models.CharField(max_length=25)),
                ('website_url', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]