"""ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter  # type: ignore
from channels.security.websocket import AllowedHostsOriginValidator  # type: ignore
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

django_asgi_app = get_asgi_application()

from live.consumers import TaskStatusConsumer  # noqa: E402, I001

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            URLRouter([path("ws/notifications", TaskStatusConsumer.as_asgi())])
        ),
    }
)
