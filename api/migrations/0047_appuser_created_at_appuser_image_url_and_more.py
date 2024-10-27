"""Generated by Django 5.1.1 on 2024-10-27 01:45."""

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0046_alter_playlist_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="appuser",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="appuser",
            name="image_url",
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name="appuser",
            name="saved_albums",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="appuser",
            name="saved_artists",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="appuser",
            name="saved_playlists",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="appuser",
            name="saved_shows",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="appuser",
            name="saved_tracks",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="appuser",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
