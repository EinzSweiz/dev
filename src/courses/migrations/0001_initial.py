# Generated by Django 5.1.1 on 2024-10-02 12:22

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "access",
                    models.CharField(
                        choices=[
                            ("anyone", "Anyone"),
                            ("email required", "Email Required"),
                        ],
                        default="anyone",
                        max_length=20,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=courses.models.handle_upload
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("published", "Published"),
                            ("coming soon", "Coming Soon"),
                            ("draft", "Draft"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
