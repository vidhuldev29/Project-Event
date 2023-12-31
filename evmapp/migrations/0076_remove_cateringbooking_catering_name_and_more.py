# Generated by Django 4.1.5 on 2023-06-18 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evmapp', '0075_alter_catering_location_alter_photography_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cateringbooking',
            name='catering_name',
        ),
        migrations.RemoveField(
            model_name='cateringbooking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='conventionbooking',
            name='convention_name',
        ),
        migrations.RemoveField(
            model_name='conventionbooking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='decorationbooking',
            name='decoration_name',
        ),
        migrations.RemoveField(
            model_name='decorationbooking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='entertainmentbooking',
            name='program_service_name',
        ),
        migrations.RemoveField(
            model_name='entertainmentbooking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='photographybooking',
            name='studio_name',
        ),
        migrations.RemoveField(
            model_name='photographybooking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='transportationbooking',
            name='travels_name',
        ),
        migrations.RemoveField(
            model_name='transportationbooking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='bus_price',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='cars_price',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='traveller_price',
        ),
        migrations.AddField(
            model_name='catering',
            name='avg_menu_charge',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='catering_booking',
            name='guest',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='photography_booking',
            name='event_type',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='transportation',
            name='avg_km_charge',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='transportation_booking',
            name='km',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='place',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='convention',
            name='place',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='AccommodationBooking',
        ),
        migrations.DeleteModel(
            name='CateringBooking',
        ),
        migrations.DeleteModel(
            name='ConventionBooking',
        ),
        migrations.DeleteModel(
            name='DecorationBooking',
        ),
        migrations.DeleteModel(
            name='EntertainmentBooking',
        ),
        migrations.DeleteModel(
            name='PhotographyBooking',
        ),
        migrations.DeleteModel(
            name='TransportationBooking',
        ),
    ]
