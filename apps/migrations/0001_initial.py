# Generated by Django 5.1.1 on 2024-10-30 05:06

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ListeningHistory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("played_at", models.DateTimeField()),
                ("logged_at", models.DateTimeField(auto_now_add=True)),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.track"
                    ),
                ),
            ],
            options={
                "ordering": ["-played_at"],
            },
        ),
    ]
