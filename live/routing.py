"""Channel Routing."""

from django.urls import re_path

from live.consumers import TaskStatusConsumer

websocket_urlpatterns = [re_path(r"ws/notifications/$", TaskStatusConsumer.as_asgi())]
