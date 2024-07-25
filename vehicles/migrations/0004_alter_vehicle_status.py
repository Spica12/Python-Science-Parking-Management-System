# Generated by Django 5.0.7 on 2024-07-24 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_remove_vehicle_is_blocked_vehicle_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('BLOCKED', 'BLOCKED'), ('UNREGISTERED', 'UNREGISTERED')], default='ACTIVE'),
        ),
    ]