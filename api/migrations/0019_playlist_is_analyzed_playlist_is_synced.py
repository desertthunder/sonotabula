# Generated by Django 5.1.1 on 2024-10-12 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_rename_artist_album_artists_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlist",
            name="is_analyzed",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="playlist",
            name="is_synced",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]