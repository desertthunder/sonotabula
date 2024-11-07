"""Playlist Filter Class."""

from curses.ascii import isdigit

from django.db import models
from rest_framework.request import Request

from api.models import Album, Playlist, Track
from core.filters import FilterMeta, FilterSet


class PlaylistFilterSet(FilterSet):
    """Filter queryset by fields available in the Playlist model."""

    def filter_name(
        self, qs: models.QuerySet, value: str, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by playlist name."""
        return qs.filter(name__icontains=value)

    def filter_public(
        self, qs: models.QuerySet, value: bool, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by public status."""
        return qs.filter(public=value)

    def filter_collaborative(
        self, qs: models.QuerySet, value: bool, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by collaborative status."""
        return qs.filter(shared=value)

    def filter_my_playlists(
        self, qs: models.QuerySet, value: str, request: Request, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by user's playlist.

        Takes owner_id as the value.
        """
        user = self.get_user(request)
        spotify_id = user.spotify_id
        return qs.filter(owner_id=spotify_id)

    def filter_is_analyzed(
        self, qs: models.QuerySet, value: int | bool, *args, **kwargs
    ) -> models.QuerySet:
        """Sort by is_active."""
        return qs.filter(is_analyzed=bool(value))

    def filter_is_synced(
        self, qs: models.QuerySet, value: int | bool
    ) -> models.QuerySet:
        """Sort by is_synced."""
        return qs.filter(is_synced=bool(value))

    def filter_private(
        self, qs: models.QuerySet, value: int | bool, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by private status."""
        return qs.filter(public=bool(value)).filter(shared=bool(value))

    def filter_num_tracks(
        self, qs: models.QuerySet, value: int, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by number of tracks."""
        return qs.annotate(num_tracks=models.Count("tracks")).filter(
            num_tracks__gte=value
        )

    def filter_num_tracks_gt(
        self, qs: models.QuerySet, value: int, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by number of tracks greater than."""
        return qs.annotate(num_tracks=models.Count("tracks")).filter(
            num_tracks__gt=value
        )

    def filter_num_tracks_lt(
        self, qs: models.QuerySet, value: int, *args, **kwargs
    ) -> models.QuerySet:
        """Filter by number of tracks less than."""
        return qs.annotate(num_tracks=models.Count("tracks")).filter(
            num_tracks__lt=value
        )

    def filter_track_name(
        self, qs: models.QuerySet, value: str, *args, **kwargs
    ) -> models.QuerySet:
        """Filter/search for a playlist by track name."""
        return qs.prefetch_related("tracks").filter(tracks__name__icontains=value)

    def sort_name(self, qs: models.QuerySet, direction: str = "asc") -> models.QuerySet:
        """Sort by playlist name."""
        if direction == "desc":
            return qs.order_by("-name")

        return qs.order_by("name")

    def sort_is_synced(
        self, qs: models.QuerySet, direction: str = "asc", *args, **kwargs
    ) -> models.QuerySet:
        """Sort by is_synced."""
        if direction == "desc":
            return qs.order_by("-is_synced")

        return qs.order_by("is_synced")

    def sort_is_analyzed(
        self, qs: models.QuerySet, direction: str = "asc"
    ) -> models.QuerySet:
        """Sort by is_active."""
        if direction == "desc":
            return qs.order_by("-is_analyzed")

        return qs.order_by("is_analyzed")

    def get_queryset(self, request: Request, *args, **kwargs) -> models.QuerySet:
        """Access initial queryset."""
        user = self.get_user(request)
        return self.Meta.default_queryset.filter(libraries__user=user)

    class Meta(FilterMeta):
        """Meta options."""

        default_queryset = Playlist.objects.all()
        filter_fields = [
            "name",
            "public",
            "collaborative",
            "my_playlists",
            "private",
            "num_tracks_gt",
            "num_tracks_lt",
            "is_analyzed",
        ]
        sort_fields = ["name", "public", "collaborative", "is_synced", "is_analyzed"]


class AlbumFilterSet(FilterSet):
    """Album filters."""

    def filter_is_analyzed(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by is_analyzed."""
        if isdigit(value) and int(value) < 2:
            return qs.filter(is_analyzed=bool(int(value)))

        raise ValueError("Invalid value for is_analyzed.")

    def filter_artist(self, qs: models.QuerySet, artist_id: str) -> models.QuerySet:
        """Filter by artist (pk)."""
        return qs.filter(artists__id=artist_id)

    def filter_released_before(
        self, qs: models.QuerySet, value: str
    ) -> models.QuerySet:
        """Filter by release date."""
        return qs.filter(release_year__lt=value)

    def filter_released_after(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by release date."""
        return qs.filter(release_year__gt=value)

    def filter_release_year(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by release year."""
        return qs.filter(release_year=value)

    def search_artist_name(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by artist."""
        return qs.filter(artists__icontains=value)

    def search_name(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Search by name."""
        return qs.filter(name__icontains=value)

    def sort_name(self, qs: models.QuerySet, direction: str = "asc") -> models.QuerySet:
        """Sort by name."""
        if direction == "desc":
            return qs.order_by("-name")

        return qs.order_by("name")

    def sort_release_year(
        self, qs: models.QuerySet, direction: str = "asc"
    ) -> models.QuerySet:
        """Sort by release date."""
        if direction == "desc":
            return qs.order_by("-release_year")

        return qs.order_by("release_year")

    def get_queryset(self, request: Request, *args, **kwargs) -> models.QuerySet:
        """Access initial queryset."""
        user = self.get_user(request)
        return (
            self.Meta.default_queryset.filter(libraries__user=user)
            .prefetch_related("artists")
            .prefetch_related("genres")
        )

    class Meta(FilterMeta):
        """Meta options."""

        default_queryset = Album.objects.all()
        filter_fields = [
            "is_analyzed",
            "artist",
            "released_before",
            "released_after",
            "release_year",
        ]
        sort_fields = ["name", "release_year"]
        search_fields = []


class TrackFilterSet(FilterSet):
    """Track Filter Class."""

    def filter_name(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by track name."""
        return qs.filter(name__icontains=value)

    def filter_artist(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by artist name."""
        return qs.prefetch_related("album__artists").filter(
            album__artists__name__icontains=value
        )

    def filter_album(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by album name."""
        return qs.prefetch_related("albums").filter(album__name__icontains=value)

    def filter_is_synced(self, qs: models.QuerySet, value: bool) -> models.QuerySet:
        """Filter by synced status."""
        return qs.filter(library__isnull=(not value))

    def filter_is_analyzed(self, qs: models.QuerySet, value: bool) -> models.QuerySet:
        """Filter by analyzed status."""
        return qs.filter(features__isnull=(not value))

    def get_queryset(self, request: Request, *args, **kwargs) -> models.QuerySet:
        """Access initial queryset."""
        qs = self.Meta.default_queryset

        if kwargs.get("playlist_pk"):
            qs = qs.filter(playlists=kwargs.get("playlist_pk"))

        if kwargs.get("include_features"):
            qs = qs.prefetch_related("features")

        if kwargs.get("include_computation"):
            qs = qs.prefetch_related("computation")

        return qs

    class Meta:
        """Track Filter options."""

        default_queryset = Track.objects.all()
        filter_fields = [
            "name",
            "artist",
            "album",
            "duration",
            "is_synced",
            "is_analyzed",
        ]
