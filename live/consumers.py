"""Channel Consumers module."""

import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer


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
                    "notification": event["notification"],
                }
            )
        )

    async def task_complete(self, event: dict) -> None:
        """Handle a task complete event."""
        await asyncio.sleep(5)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "task_complete",
                    "notification": event["notification"],
                }
            )
        )
