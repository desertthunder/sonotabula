"""Channel Consumers module."""

import enum
import json

import pydantic
from channels.db import database_sync_to_async  # type: ignore
from channels.generic.websocket import AsyncJsonWebsocketConsumer  # type: ignore
from loguru import logger
from pydantic import BaseModel

from core.models import AppUser
from live.models import Acknowledgement, Notification


class CustomCloseCode(enum.IntEnum):
    """Custom Close Code."""

    INVALID_JSON = 4000
    INVALID_MESSAGE_FORMAT = 4001
    USER_DOES_NOT_EXIST = 4002
    NOTIFICATION_DOES_NOT_EXIST = 4003


class WebsocketMessage(BaseModel):
    """Websocket Message Model."""

    user_id: str
    notification_id: str
    message: str | None = None


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """Notification Consumer."""

    async def connect(self) -> None:
        """Connect to client WS."""
        logger.debug("Connected to client WS")

        await self.accept()

    async def disconnect(self, close_code: int | None = None) -> None:
        """Disconnect."""
        logger.info("Disconnected from client WS")

        await self.close(code=close_code)

    async def send_message(self, message: dict) -> None:
        """Send message."""
        logger.debug(f"Sending message: {message}")

        await self.send_json(message)

    async def receive(self, text_data: str) -> None:
        """Receive message."""
        try:
            data = json.loads(text_data)
            message = WebsocketMessage(**data)

            user = await self._get_user(message.user_id)
            notification = await self._get_notification(message.notification_id)

            await self._create_ack_record(user, notification, message.message)
            await self.send_json({"status": "acknowledged"})

        except (
            pydantic.ValidationError,
            json.JSONDecodeError,
            ValueError,
        ):
            await self.send_json({"error": "Invalid message format"})
            await self.close()

    async def _get_user(self, user_id: str) -> AppUser:
        try:
            user = await database_sync_to_async(AppUser.objects.get)(id=user_id)
        except AppUser.DoesNotExist as e:
            logger.error(f"User {user_id} does not exist")
            raise pydantic.ValidationError from e

        return user

    async def _get_notification(self, notification_id: str) -> Notification:
        try:
            notification = await database_sync_to_async(
                Notification.objects.get,
            )(id=notification_id)
        except Notification.DoesNotExist as e:
            logger.error(f"Notification {notification_id} does not exist")
            raise pydantic.ValidationError from e

        return notification

    async def _create_ack_record(
        self,
        user: AppUser,
        notification: Notification,
        message: str | None = None,
    ) -> None:
        ack = await database_sync_to_async(Acknowledgement.objects.create)(
            user=user, notification=notification, message=message
        )

        logger.debug(f"Created Acknowledgement: {ack}")
