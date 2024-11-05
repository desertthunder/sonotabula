"""Playback urls."""

from django.urls import path

from apps import views

urlpatterns = [
    path("saved", views.UserSavedItemsView.as_view(), name="saved-items"),
    path("recent", views.ListeningHistoryView.as_view(), name="listening-history"),
]
