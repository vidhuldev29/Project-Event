# Generated by Django 4.1.5 on 2023-03-03 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0016_alter_users_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='endtime',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='starttime',
            new_name='start_time',
        ),
        migrations.AlterField(
            model_name='test',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
