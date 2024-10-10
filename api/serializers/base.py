"""Serializer Base Classes."""

import typing

from pydantic import BaseModel


class Serializer(BaseModel):
    """Base class for serializing data."""

    @classmethod
    def mappings(cls: type[typing.Self]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def nullable_fields(cls: type[typing.Self]) -> tuple:
        """Fields that can be null."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def map_response(cls: type[typing.Self], response: dict) -> dict:
        """Map JSON data to class properties."""
        data = {}

        for key, value in cls.mappings().items():
            path = value.split(".")
            prop = response.copy()

            for p in path:
                if p.isdigit() and isinstance(prop, list):
                    i = int(p)
                    prop = prop[i]
                elif isinstance(prop, dict) and prop.get(p):
                    prop = prop.get(p)  # type: ignore
            if isinstance(prop, dict):
                prop = ""  # type: ignore

            if prop is not None:
                data[key] = prop

        for field in cls.nullable_fields():
            if field not in data:
                data[field] = None  # type: ignore

        return data

    @classmethod
    def get(cls: type[typing.Self], response: dict) -> typing.Self:
        """Create a Serializer object from JSON data."""
        data: dict = cls.map_response(response)

        return cls(**data)

    @classmethod
    def list(
        cls: type[typing.Self], response: list[dict]
    ) -> typing.Iterable[typing.Self]:
        """Create a list of Serializer objects from JSON data."""
        for item in response:
            yield cls.get(item)
