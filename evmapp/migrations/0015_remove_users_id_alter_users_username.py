# Generated by Django 4.1.5 on 2023-02-25 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0014_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='id',
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=25, primary_key=True, serialize=False),
        ),
    ]
