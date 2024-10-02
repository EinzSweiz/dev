# Generated by Django 5.1.1 on 2024-10-02 17:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_remove_lesson_video_lesson_can_preview_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="thumbnail",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="image"
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="video",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="video"
            ),
        ),
    ]
