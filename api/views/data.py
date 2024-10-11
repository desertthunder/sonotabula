"""Data views."""

from django.http import (
    HttpResponse,
    JsonResponse,
)
from rest_framework.request import Request as DRFRequest

from api.serializers.data import UserSavedItems
from api.views.base import SpotifyDataView


class UserSavedItemsView(SpotifyDataView):
    """User saved items view."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get user saved items."""
        user = self.get_user(request)
        data = self.data_service.fetch_saved_items(user, 1)
        items = UserSavedItems.get(data)
        return JsonResponse({"data": items.model_dump()})
