"""Notification serializers."""

import datetime
import json
import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from live.models import Notification


class NotificationSerializer(BaseModel):
    """Notification serializer."""

    id: uuid.UUID
    user_id: int

    resource_id: uuid.UUID | None = None
    resource: str
    operation: str

    task_id: str
    task_name: str
    task_status: str

    extras: dict[str, str]

    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_model(
        cls: type["NotificationSerializer"], notification: "Notification"
    ) -> "NotificationSerializer":
        """Create a serializer from a model instance."""
        extras = json.loads(notification.extras) if notification.extras else {}

        return cls(
            id=notification.id,
            user_id=notification.user_id,
            resource_id=notification.resource_id,
            resource=notification.resource,
            operation=notification.operation,
            task_id=notification.task_id,
            task_name=notification.task_name,
            task_status=notification.task_status,
            extras=extras,
            created_at=notification.created_at,
            updated_at=notification.updated_at,
        )
