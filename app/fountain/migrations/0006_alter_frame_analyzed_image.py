# Generated by Django 4.1 on 2023-03-13 12:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fountain", "0005_fountain_code_fountain_music"),
    ]

    operations = [
        migrations.AlterField(
            model_name="frame",
            name="analyzed_image",
            field=models.URLField(
                blank=True,
                error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
                max_length=250,
                null=True,
            ),
        ),
    ]
