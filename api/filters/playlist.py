"""Playlist Filter Class."""

from django.db import models
from rest_framework.request import Request

from api.models.playlist import Playlist
from api.models.users import AppUser


class PlaylistFilterSet:
    """Filter queryset by fields available in the Playlist model."""

    def get_user(self, request: Request) -> AppUser:
        """Get the authenticated user."""
        user = request.user
        if isinstance(user, AppUser):
            return user
        else:
            raise ValueError("User is not authenticated.")

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

    def filter_is_analyzed(self, qs: models.QuerySet) -> models.QuerySet:
        """Sort by is_active."""
        return qs.filter(is_analyzed=True)

    def filter_is_synced(self, qs: models.QuerySet) -> models.QuerySet:
        """Sort by is_synced."""
        return qs.filter(is_synced=True)

    def filter_private(self, qs: models.QuerySet) -> models.QuerySet:
        """Filter by private status."""
        return qs.filter(public=False).filter(shared=False)

    def filter_num_tracks(self, qs: models.QuerySet, value: int) -> models.QuerySet:
        """Filter by number of tracks."""
        return qs.annotate(num_tracks=models.Count("tracks")).filter(
            num_tracks__gte=value
        )

    def sort_name(self, qs: models.QuerySet) -> models.QuerySet:
        """Sort by playlist name."""
        return qs.order_by("name")

    def sort_is_synced(self, qs: models.QuerySet) -> models.QuerySet:
        """Sort by is_synced."""
        return qs.order_by("is_synced")

    def sort_is_analyzed(self, qs: models.QuerySet) -> models.QuerySet:
        """Sort by is_active."""
        return qs.order_by("is_analyzed")

    def get_queryset(
        self, request: Request, queryset: models.QuerySet | None = None
    ) -> models.QuerySet:
        """Access initial queryset."""
        user = self.get_user(request)

        if queryset is None:
            qs = self.Meta.default_queryset.filter(libraries__user=user)
        else:
            qs = queryset.filter(libraries__user=user)

        return qs

    def __call__(
        self, request: Request, queryset: models.QuerySet | None = None
    ) -> models.QuerySet:
        """Return the filtered queryset."""
        qs = self.get_queryset(request, queryset)

        params = request.query_params.copy()
        sort_params = params.pop("sort", None)

        for key, value in params.items():
            if key in self.Meta.filter_fields:
                qs = getattr(self, f"filter_{key}")(qs, value)

        if sort_params:
            for key in sort_params:
                if key in self.Meta.sort_fields:
                    qs = getattr(self, f"sort_{key}")(qs)
        return qs

    class Meta:
        """Meta options."""

        default_queryset = Playlist.objects.all()
        filter_fields = ["name", "public", "collaborative", "my_playlist", "private"]
        sort_fields = ["name", "public", "collaborative", "is_synced", "is_analyzed"]
