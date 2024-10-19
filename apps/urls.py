"""Playback urls."""

from django.urls import path

from apps import views

urlpatterns = [
    path("recent/", views.ListeningHistoryView.as_view(), name="listening-history"),
]
