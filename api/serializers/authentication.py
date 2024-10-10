"""Pydantic models for authentication."""

import datetime

from django.utils import timezone

from api.serializers.base import Serializer


class AccessToken(Serializer):
    """Spotify Access Token Response Data."""

    access_token: str
    refresh_token: str
    token_type: str
    token_expiry: datetime.datetime

    @classmethod
    def mappings(cls: type["AccessToken"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "token_type": "token_type",
        }

    @classmethod
    def nullable_fields(cls: type["AccessToken"]) -> tuple[str]:
        """Fields that can be null."""
        return ("token_expiry",)

    @classmethod
    def get(cls: type["AccessToken"], response: dict) -> "AccessToken":
        """Create a Serializer object from JSON data."""
        data: dict = cls.map_response(response)

        if "token_expiry" in data and data.get("token_expiry"):
            token_expiry = int(data["token_expiry"])
            data["token_expiry"] = timezone.now() + datetime.timedelta(
                seconds=token_expiry
            )
        elif "expires_in" in response and response.get("expires_in"):
            token_expiry = int(response["expires_in"])
            data["token_expiry"] = timezone.now() + datetime.timedelta(
                seconds=token_expiry
            )

        return cls(**data)


class CurrentUser(Serializer):
    """Spotify Current User Data."""

    display_name: str
    email: str
    id: str

    @classmethod
    def mappings(cls: type["CurrentUser"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "display_name": "display_name",
            "email": "email",
            "id": "id",
        }

    @classmethod
    def nullable_fields(cls: type["CurrentUser"]) -> tuple[str]:
        """Fields that can be null."""
        return ("",)
