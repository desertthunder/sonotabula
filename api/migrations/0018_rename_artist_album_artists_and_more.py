# Generated by Django 5.1.1 on 2024-10-12 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_rename_identity_album_id_rename_identity_artist_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="album",
            old_name="artist",
            new_name="artists",
        ),
        migrations.RenameField(
            model_name="track",
            old_name="album_id",
            new_name="album",
        ),
    ]
