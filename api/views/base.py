"""API View base classes.

TODO - Since there is only the single mixin remaining, this
should be moved to the core app.
"""

from rest_framework.request import Request as DRFRequest

from core.models import AppUser


class GetUserMixin:
    """Mixin for getting the user from the request."""

    def get_user(self, request: DRFRequest) -> AppUser:
        """Get the user from the request object.

        This method ensures that we're not using an
        AnonymousUser instance, as the QuerySet will
        raise a AppUser.DoesNotExist exception if we do.
        """
        return AppUser.objects.get(pk=request.user.pk)
