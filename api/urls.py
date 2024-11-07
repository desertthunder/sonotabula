"""API Routing."""

from django.urls import include, path

from api.views import auth
from core.views import ProfileViewSet

urlpatterns = [
    path("login", auth.LoginView.as_view(), name="login"),
    path("validate", auth.ValidateView.as_view(), name="validate-token"),
    path("v1/playback/", include("apps.urls")),
    path("v1/browser/", include("browser.urls")),
    path("v1/library/", include("library.urls")),
    path("v1/profile", ProfileViewSet.as_view({"get": "retrieve"}), name="profile"),
]
