# Generated by Django 5.0.7 on 2024-07-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parking_service", "0014_alter_parkingsession_vehicle"),
    ]

    operations = [
        migrations.AddField(
            model_name="parkingsession",
            name="vehicle_plate_number",
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]