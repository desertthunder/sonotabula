"""Notification signals and receiver functions."""

import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer  # type: ignore
from django.dispatch import Signal, receiver

from live.models import Notification

notification_created = Signal()
notification_updated = Signal()


@receiver(notification_created)
def notification_created_handler(
    sender: type[Notification], instance: Notification, *args, **kwargs
) -> None:
    """Handle the creation of a notification."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "task_started",
            "notification": {
                "id": str(instance.id),
                "task_id": instance.task_id,
                "task_name": instance.task_name,
                "task_status": instance.task_status,
                "extras": instance.extras,
            },
        },
    )


@receiver(notification_updated)
def notification_updated_handler(
    sender: type[Notification], instance: Notification, **kwargs
) -> None:
    """Handle the update of a notification."""
    channel_layer = get_channel_layer()

    time.sleep(5)  # We need to wait for the task to be updated

    if task_result := instance.task_result:
        instance.refresh_from_db()
        task_result.refresh_from_db()

    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "task_complete",
            "notification": {
                "id": str(instance.id),
                "task_id": instance.task_id,
                "task_name": instance.task_name,
                "task_status": instance.task_status,
                "extras": instance.extras,
            },
        },
    )
