# Generated by Django 4.1.5 on 2023-03-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0015_remove_users_id_alter_users_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]