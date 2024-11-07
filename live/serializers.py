"""Notification serializers."""

import json
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from live.models import Notification


class NotificationSerializer(BaseModel):
    """Notification serializer."""

    id: str
    user_id: int

    resource_id: str | None = None
    resource: str
    operation: str

    task_id: str

    extras: dict[str, str] | str

    @classmethod
    def from_model(
        cls: type["NotificationSerializer"], notification: "Notification"
    ) -> "NotificationSerializer":
        """Create a serializer from a model instance."""
        extras = json.dumps(notification.extras if notification.extras else {})

        return cls(
            id=str(notification.id),
            user_id=notification.user_id,
            resource_id=str(notification.resource_id),
            resource=notification.resource,
            operation=notification.operation,
            task_id=notification.task_id,
            extras=extras,
        )
