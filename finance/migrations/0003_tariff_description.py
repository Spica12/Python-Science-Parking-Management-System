# Generated by Django 5.0.7 on 2024-07-24 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_tariff_end_date_alter_tariff_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]