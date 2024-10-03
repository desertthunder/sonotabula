"""API Routing."""

from django.urls import path

from api.views import LoginView, ValidateView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("validate", ValidateView.as_view(), name="validate-token"),
]
