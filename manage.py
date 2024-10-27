#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# ruff: noqa
import logging
import os
import sys

from loguru import logger


def init_logger():
    colors = {
        "TRACE": "green",
        "DEBUG": "blue",
        "INFO": "cyan",
        "SUCCESS": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "magenta",
    }

    def formatter(record) -> str:
        log_level = record["level"].name
        color = colors.get(log_level, "reset")
        return "{time} | <{color}>[{level:<8}]</{color}> | {name}:{function}:{line} | {message}".format(
            color=color, **record
        )

    logging.getLogger("daphne").setLevel(logging.INFO)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format=formatter,
    )


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

    init_logger()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
