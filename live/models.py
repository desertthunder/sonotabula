"""Async models for the live app."""

import datetime

from django.db import models
from django_celery_results.models import GroupResult, TaskResult
from django_stubs_ext.db.models import TypedModelMeta

from core.mixins import Model


class Acknowledgement(Model):
    """Client ack of notification."""

    notification = models.OneToOneField(
        "Notification",
        on_delete=models.CASCADE,
        related_name="acknowledgement",
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        "core.AppUser",
        on_delete=models.CASCADE,
        related_name="acknowledgements",
        null=False,
        blank=False,
    )

    @property
    def acknowledged_at(self) -> datetime.datetime:
        """Return the time the ack was made."""
        return self.created_at


class Notification(Model):
    """A wrapper around a task's result and user.

    This is used to represent the time at which a
    task was executed and the user that should be
    notified of the result.
    """

    task_result = models.OneToOneField(
        TaskResult,
        on_delete=models.PROTECT,
        related_name="notification",
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        "core.AppUser",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=False,
        blank=False,
    )

    group_result = models.ForeignKey(
        GroupResult,
        on_delete=models.PROTECT,
        related_name="notification",
        null=True,
        blank=True,
    )

    extras = models.JSONField(null=True, blank=True)

    def ack(self) -> Acknowledgement:
        """Acknowledge the notification."""
        return Acknowledgement.objects.create(
            notification=self,
            user=self.user,
        )

    @property
    def task_id(self) -> str:
        """Return the task id."""
        if task := self.task_result:
            return task.task_id
        elif group := self.group_result:
            return group.group_id

        raise ValueError("Notification has no task or group result")

    @property
    def task_name(self) -> str:
        """Return the task name."""
        if task := self.task_result:
            return task.task_name
        elif group := self.group_result:
            return group.group_id

        raise ValueError("Notification has no task or group result")

    @property
    def task_status(self) -> str:
        """Return the task status."""
        if task := self.task_result:
            return task.status
        elif group := self.group_result:
            return "PENDING" if not group.date_done else "SUCCESS"

        raise ValueError("Notification has no task or group result")

    @property
    def acked(self) -> bool:
        """Return the acknowledged status."""
        return hasattr(self, "acknowledgement")

    # Constraints: Either task or group must be set
    class Meta(TypedModelMeta):
        """Notification metadata class.

        Defines constraints.
        """

        ordering = ["user", "-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(task_result__isnull=False)
                | models.Q(group_result__isnull=False),
                name="notification_task_or_group",
            )
        ]
