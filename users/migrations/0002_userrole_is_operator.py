# Generated by Django 5.0.7 on 2024-07-24 07:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0001_initial"),
    ]


    operations = [
        migrations.AddField(
            model_name="userrole",
            name="is_operator",
            field=models.BooleanField(default=False),
        ),
    ]
