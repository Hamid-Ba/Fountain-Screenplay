# Generated by Django 4.1 on 2023-03-15 12:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fountain", "0006_alter_frame_analyzed_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fountain",
            name="packages",
            field=models.ManyToManyField(
                blank=True, related_name="fountains", to="fountain.package"
            ),
        ),
    ]
