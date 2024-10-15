"""Track FilterSet."""

from django.db import models
from rest_framework.request import Request

from api.filters.base import FilterSet
from api.models import Track


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
