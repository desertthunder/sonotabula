"""API Views."""

from rest_framework import views
from rest_framework.request import Request


class CallbackMixin(views.GenericView):
    """Handle Callback Mixin."""

    def callback(self, request: Request) -> None:
        """OAuth2 Callback."""
        authorization_code = request.query_params.get("code")

        if not authorization_code:
            return

        pass


class AuthenticateMixin(views.GenericView):
    """Handle Authentication Mixin."""

    def authenticate(self, request: Request) -> None:
        """Authenticate.

        Create a JWT and redirect to the frontend.

        i.e. /dashboard?token=JWT - The client is expected to
        store the JWT in localStorage and redirect to /dashboard.
        """
        pass


class SignupView(views.APIView, CallbackMixin):
    """Signup View."""

    pass


class LoginView(views.APIView, CallbackMixin):
    """Login View."""

    pass
