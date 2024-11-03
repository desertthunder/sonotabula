"""Notification dispatch tasks."""

from celery import Task, shared_task
from django_celery_results.models import GroupResult, TaskResult
from loguru import logger

from live.models import Notification
from live.signals import notification_created, notification_updated


@shared_task(bind=True)
def start_task_execution(
    self: Task, task_id: str, user_id: int, extras: dict[str, str]
) -> str:
    """Start the task execution."""
    task_result = TaskResult.objects.get(task_id=task_id)
    notification = Notification.objects.create(
        user_id=user_id, task_result=task_result, extras=extras
    )

    logger.info(f"Task {task_result.task_id} started")
    logger.info(f"Notification {notification.id} created")

    notification_created.send(sender=Notification, instance=notification)

    return task_id


@shared_task(bind=True)
def start_group_execution(self: Task, user_id: int, extras: dict[str, str]) -> None:
    """Start the group execution."""
    group_result = GroupResult.objects.get(group_id=self.request.id)
    notification = Notification.objects.create(
        user_id=user_id, group_result=group_result, extras=extras
    )

    logger.info(f"Task {group_result.group_id} started")
    logger.info(f"Notification {notification.id} created")

    notification_created.send(sender=Notification, instance=notification)


@shared_task
def task_complete(task_id: str) -> None:
    """Complete the task."""
    notification = Notification.objects.get(task_result__task_id=task_id)
    notification_updated.send(sender=Notification, instance=notification)
