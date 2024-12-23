# Generated by Django 5.1.1 on 2024-10-30 05:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="analysis",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="artist",
            name="albums",
            field=models.ManyToManyField(related_name="artists", to="api.album"),
        ),
        migrations.AddField(
            model_name="computation",
            name="analysis",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="data",
                to="api.analysis",
            ),
        ),
        migrations.AddField(
            model_name="artist",
            name="genres",
            field=models.ManyToManyField(related_name="artists", to="api.genre"),
        ),
        migrations.AddField(
            model_name="album",
            name="genres",
            field=models.ManyToManyField(related_name="albums", to="api.genre"),
        ),
        migrations.AddField(
            model_name="library",
            name="artists",
            field=models.ManyToManyField(related_name="libraries", to="api.artist"),
        ),
        migrations.AddField(
            model_name="library",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="library",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="libraries",
            field=models.ManyToManyField(related_name="albums", to="api.library"),
        ),
        migrations.AddField(
            model_name="playlist",
            name="libraries",
            field=models.ManyToManyField(related_name="playlists", to="api.library"),
        ),
        migrations.AddField(
            model_name="playlist",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="playlists",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="computation",
            name="playlist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="computation",
                to="api.playlist",
            ),
        ),
        migrations.AddField(
            model_name="analysis",
            name="playlist",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysis",
                to="api.playlist",
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="album",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tracks",
                to="api.album",
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="playlists",
            field=models.ManyToManyField(related_name="tracks", to="api.playlist"),
        ),
        migrations.AddField(
            model_name="library",
            name="tracks",
            field=models.ManyToManyField(related_name="libraries", to="api.track"),
        ),
        migrations.AddField(
            model_name="analysis",
            name="tracks",
            field=models.ManyToManyField(related_name="analyses", to="api.track"),
        ),
        migrations.AddField(
            model_name="trackfeatures",
            name="track",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="features",
                to="api.track",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="playlist",
            unique_together={("spotify_id", "user")},
        ),
    ]
