"""Generated by Django 5.1.1 on 2024-10-30 05:06."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("live", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="acknowledgement",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="acknowledgements",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="acknowledgement",
            name="notification",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ack",
                to="live.notification",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="operation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to="live.operation",
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="resource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="operations",
                to="live.resource",
            ),
        ),
    ]
