"""Album filterset."""

from curses.ascii import isdigit

from django.db import models
from rest_framework.request import Request

from api.filters.base import FilterMeta, FilterSet
from api.models import Album


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
