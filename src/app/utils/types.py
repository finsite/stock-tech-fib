"""Shared enums and validation helpers used across the application.

NOTE: This file is maintained in `repo-utils-shared/src/app/utils/types.py`
and should be synchronized across repositories using the sync script.
Do not modify it directly in individual repositories.
"""

from enum import Enum
from typing import Any, TypedDict


class OutputMode(str, Enum):
    """Available output modes for processed data."""

    QUEUE = "queue"
    LOG = "log"
    STDOUT = "stdout"
    REST = "rest"
    S3 = "s3"
    DATABASE = "database"


class PollerType(str, Enum):
    """Defines the domain of the poller for routing and behavior."""

    STOCK = "stock"
    SENTIMENT = "sentiment"
    ALT = "alt"
    CRYPTO = "crypto"
    FUND = "fund"
    ANALYSIS = "analysis"
    BACKTEST = "backtest"
    UI = "ui"


class ValidatedMessage(TypedDict):
    """Validated and enriched message with required structure."""

    symbol: str
    timestamp: str
    data: dict[str, Any]


def validate_dict(data: dict[str, Any], required_keys: list[str]) -> bool:
    """Check that all required keys are present in the dictionary.

    Args:
        data: The dictionary to validate.
        required_keys: Keys that must exist in the dictionary.

    Returns:
        True if all required keys are present, False otherwise.
    """
    return all(k in data for k in required_keys)


def validate_list_of_dicts(data: Any, required_keys: list[str]) -> bool:
    """Validate that the input is a list of dicts, each with required keys.

    Args:
        data: The object to validate.
        required_keys: Keys that must exist in each dictionary.

    Returns:
        True if input is a list of valid dicts, False otherwise.
    """
    if not isinstance(data, list):
        return False
    return all(isinstance(item, dict) and validate_dict(item, required_keys) for item in data)


def is_valid_payload(data: Any) -> bool:
    """Perform basic schema validation for a generic payload.

    Args:
        data: The input data to validate.

    Returns:
        True if the input is a dict with minimum expected structure.
    """
    return isinstance(data, dict) and "symbol" in data and "timestamp" in data


def is_valid_batch(data: Any) -> bool:
    """Validate a batch of payloads.

    Args:
        data: The input to validate.

    Returns:
        True if input is a list of valid payload dictionaries.
    """
    return validate_list_of_dicts(data, ["symbol", "timestamp"])
