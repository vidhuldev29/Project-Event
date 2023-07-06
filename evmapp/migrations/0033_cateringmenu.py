# Generated by Django 4.1.5 on 2023-04-29 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0032_catering'),
    ]

    operations = [
        migrations.CreateModel(
            name='cateringmenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.TextField()),
                ('catering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evmapp.catering')),
            ],
        ),
    ]
