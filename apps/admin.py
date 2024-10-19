"""Admin configuration for the apps."""

from django.contrib import admin

from apps.models import ListeningHistory

# Register your models here.

admin.register(ListeningHistory)
