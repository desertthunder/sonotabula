"""Playlist Filter Class."""

from django.db import models
from rest_framework.request import Request

from api.filters.base import FilterMeta, FilterSet
from api.models.playlist import Playlist


class PlaylistFilterSet(FilterSet):
    """Filter queryset by fields available in the Playlist model."""

    def filter_name(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by playlist name."""
        return qs.filter(name__icontains=value)

    def filter_public(self, qs: models.QuerySet, value: bool) -> models.QuerySet:
        """Filter by public status."""
        return qs.filter(public=value)

    def filter_collaborative(self, qs: models.QuerySet, value: bool) -> models.QuerySet:
        """Filter by collaborative status."""
        return qs.filter(shared=value)

    def filter_my_playlist(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter by user's playlist.

        Takes owner_id as the value.
        """
        return qs.filter(owner_id=value)

    def filter_is_analyzed(
        self, qs: models.QuerySet, value: int | bool
    ) -> models.QuerySet:
        """Sort by is_active."""
        return qs.filter(is_analyzed=bool(value))

    def filter_is_synced(
        self, qs: models.QuerySet, value: int | bool
    ) -> models.QuerySet:
        """Sort by is_synced."""
        return qs.filter(is_synced=bool(value))

    def filter_private(self, qs: models.QuerySet, value: int | bool) -> models.QuerySet:
        """Filter by private status."""
        return qs.filter(public=bool(value)).filter(shared=bool(value))

    def filter_num_tracks(self, qs: models.QuerySet, value: int) -> models.QuerySet:
        """Filter by number of tracks."""
        return qs.annotate(num_tracks=models.Count("tracks")).filter(
            num_tracks__gte=value
        )

    def filter_num_tracks_gt(self, qs: models.QuerySet, value: int) -> models.QuerySet:
        """Filter by number of tracks greater than."""
        return qs.annotate(num_tracks=models.Count("tracks")).filter(
            num_tracks__gt=value
        )

    def filter_num_tracks_lt(self, qs: models.QuerySet, value: int) -> models.QuerySet:
        """Filter by number of tracks less than."""
        return qs.annotate(num_tracks=models.Count("tracks")).filter(
            num_tracks__lt=value
        )

    def filter_track_name(self, qs: models.QuerySet, value: str) -> models.QuerySet:
        """Filter/search for a playlist by track name."""
        return qs.prefetch_related("tracks").filter(tracks__name__icontains=value)

    def sort_name(self, qs: models.QuerySet, direction: str = "asc") -> models.QuerySet:
        """Sort by playlist name."""
        if direction == "desc":
            return qs.order_by("-name")

        return qs.order_by("name")

    def sort_is_synced(
        self, qs: models.QuerySet, direction: str = "asc"
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
            "my_playlist",
            "private",
            "num_tracks_gt",
            "num_tracks_lt",
        ]
        sort_fields = ["name", "public", "collaborative", "is_synced", "is_analyzed"]
