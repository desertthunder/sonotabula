"""Utility functions."""

import time


def get_current_unix_timestamp() -> int:
    """Return the current Unix timestamp."""
    return int(time.time())
