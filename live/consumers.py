"""Channel Consumers module."""

import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from loguru import logger

from live.serializers import NotificationSerializer


class TaskStatusConsumer(AsyncWebsocketConsumer):
    """Websocket consumer for task status updates."""

    groups = ["task_updates"]

    async def connect(self) -> None:
        """Connect the websocket."""
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """Disconnect the websocket."""
        await self.close()

    async def task_started(self, event: dict) -> None:
        """Handle a task started event."""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "task_started",
                    "notification": NotificationSerializer(
                        **json.loads(event["notification"])
                    ).model_dump(),
                }
            )
        )

    async def task_complete(self, event: dict) -> None:
        """Handle a task complete event."""
        await asyncio.sleep(5)

        logger.debug("Task complete event received")

        await self.send(
            text_data=json.dumps(
                {
                    "type": "task_complete",
                    "notification": NotificationSerializer(
                        **json.loads(event["notification"])
                    ).model_dump(),
                }
            )
        )
