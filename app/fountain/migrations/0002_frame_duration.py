# Generated by Django 4.1 on 2023-03-11 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fountain", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="frame",
            name="duration",
            field=models.DurationField(blank=True, null=True),
        ),
    ]
