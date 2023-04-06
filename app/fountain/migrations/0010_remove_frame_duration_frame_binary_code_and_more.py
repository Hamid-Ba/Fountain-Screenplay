# Generated by Django 4.1 on 2023-04-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fountain", "0009_alter_fountain_packages"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="frame",
            name="duration",
        ),
        migrations.AddField(
            model_name="frame",
            name="binary_code",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="frame",
            name="reverse_binary_code",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="package",
            name="is_reverse",
            field=models.BooleanField(default=False),
        ),
    ]
