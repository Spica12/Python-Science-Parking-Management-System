# Generated by Django 5.0.7 on 2024-07-28 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parking_service", "0015_parkingsession_vehicle_plate_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parkingsession",
            name="vehicle_plate_number",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
