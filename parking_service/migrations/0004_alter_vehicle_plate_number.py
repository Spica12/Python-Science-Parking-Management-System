# Generated by Django 5.0.7 on 2024-07-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_service', '0003_remove_licenseplate_user_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='plate_number',
            field=models.CharField(max_length=10),
        ),
    ]
