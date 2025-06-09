"""Shared enums and validation helpers used across the application."""

from enum import Enum
from typing import Any


class OutputMode(str, Enum):
    """Available output modes for processed data."""

    QUEUE = "queue"
    LOG = "log"
    STDOUT = "stdout"
    REST = "rest"
    S3 = "s3"
    DATABASE = "database"


class PollerType(str, Enum):
    """Defines the domain of the poller for routing/behavior."""

    STOCK = "stock"
    SENTIMENT = "sentiment"
    ALT = "alt"


def validate_dict(data: dict[str, Any], required_keys: list[str]) -> bool:
    """
    Check that all required keys are present in the dictionary.

    Parameters
    ----------
    data : dict[str, Any]
        The dictionary to validate.
    required_keys : list[str]
        A list of keys that must be present in the dictionary.

    Returns
    -------
    bool
        True if all required keys are present, False otherwise.
    """
    if not isinstance(data, dict):
        return False
    return all(k in data for k in required_keys)
