"""Notification signals and receiver functions.

Handlers take the notification instance and send them to
the channel layer/consumer.
"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer  # type: ignore
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django_celery_results.models import TaskResult

from live.models import Notification
from live.serializers import NotificationSerializer

notify_start = Signal()
notify_success = Signal()
notify_failure = Signal()


@receiver(post_save, sender=TaskResult)
def task_result_post_save_handler(
    sender: type[TaskResult], instance: TaskResult, created: bool, *args, **kwargs
) -> None:
    """Create relationship between TaskResult and Notification."""
    if notification := Notification.objects.filter(task_id=instance.task_id).first():
        notification.task_result = instance
        notification.save()


@receiver(notify_start)
def notify_start_handler(
    sender: type[Notification], instance: Notification, *args, **kwargs
) -> None:
    """Handle the start notification."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "task_started",
            "notification": NotificationSerializer.from_model(
                instance,
            ).model_dump_json(),
        },
    )


@receiver(notify_success)
def notify_success_handler(
    sender: type[Notification], instance: Notification, *args, **kwargs
) -> None:
    """Handle the success notification."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "task_complete",
            "notification": NotificationSerializer.from_model(
                instance,
            ).model_dump_json(),
        },
    )


@receiver(notify_failure)
def notify_failure_handler(
    sender: type[Notification], instance: Notification, *args, **kwargs
) -> None:
    """Handle the failure notification."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "task_failed",
            "notification": NotificationSerializer.from_model(
                instance,
            ).model_dump_json(),
        },
    )
