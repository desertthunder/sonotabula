"""Async models for the browser app."""

from django.db import models

from core.mixins import Model


class ResourceType(models.TextChoices):
    """Resource type choices."""

    Playlist = "PL", "Playlist"
    Album = "AL", "Album"
    Track = "TR", "Track"
    Artist = "AR", "Artist"
    User = "US", "User"
    Operation = "OP", "Operation"


class Resource(Model):
    """Join table for resources and notifications."""

    resource_id = models.UUIDField(blank=False, null=False)
    type = models.CharField(
        max_length=2,
        choices=ResourceType.choices,
        null=False,
        blank=False,
    )


class Operation(Model):
    """An operation model."""

    class OperationType(models.TextChoices):
        """Operation type choices."""

        Analyze = "AN", "Analyze"
        Sync = "SY", "Sync"
        Compute = "CO", "Compute"

    class OperationStatus(models.TextChoices):
        """Notification type choices."""

        Started = "ST", "Started"
        Pending = "PD", "Pending"
        Completed = "CP", "Completed"
        Warning = "WN", "Warning"
        Error = "ER", "Error"

    type = models.CharField(
        max_length=2,
        choices=OperationType.choices,
        null=False,
        blank=False,
    )
    status = models.CharField(
        max_length=2,
        choices=OperationStatus.choices,
        null=False,
        blank=False,
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="operations",
    )

    def __str__(self) -> str:
        """Return the type and status of the operation."""
        type = self.OperationType(self.type).label
        status = self.OperationStatus(self.status).label

        return f"{type} - {status}"


class Acknowledgement(Model):
    """Client ack of notification."""

    message = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Optional message from the user.",
    )

    notification = models.OneToOneField(
        "Notification",
        on_delete=models.CASCADE,
        related_name="ack",
        null=False,
        blank=False,
    )

    client = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=(("WEB", "Web"), ("MOBILE", "Mobile")),
    )

    user = models.ForeignKey(
        "core.AppUser",
        on_delete=models.CASCADE,
        related_name="acknowledgements",
        null=False,
        blank=False,
    )


class Notification(Model):
    """A notification model."""

    message = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(
        "core.AppUser",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=False,
        blank=False,
    )
    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=False,
        blank=False,
    )

    @property
    def resource(self) -> Resource:
        """Return the resource of the notification."""
        return self.operation.resource

    def __str__(self) -> str:
        """Return the message of the notification."""
        return self.message
