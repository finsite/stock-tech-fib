"""Shared enums and validation helpers used across the application.

NOTE: This file is maintained in `repo-utils-shared/src/app/utils/types.py`
and should be synchronized across repositories using the sync script.
Do not modify it directly in individual repositories.
"""

from enum import Enum
from typing import Any, Literal, TypedDict


class OutputMode(str, Enum):
    """Available output destinations for processed data."""

    QUEUE = "queue"
    LOG = "log"
    STDOUT = "stdout"
    REST = "rest"
    S3 = "s3"
    DATABASE = "database"


class PollerType(str, Enum):
    """Available poller domains for routing and specialized behavior."""

    STOCK = "stock"
    SENTIMENT = "sentiment"
    ALT = "alt"
    CRYPTO = "crypto"
    FUND = "fund"
    ANALYSIS = "analysis"
    BACKTEST = "backtest"
    UI = "ui"


class ValidatedMessage(TypedDict):
    """A validated message containing required fields."""

    symbol: str
    timestamp: str
    data: dict[str, Any]


class TradeEvent(TypedDict, total=False):
    """Represents a simulated trade for paper trading output."""

    symbol: str
    action: Literal["BUY", "SELL"]
    quantity: float
    price: float
    timestamp: str
    strategy_id: str
    notes: str


class DatabaseRow(TypedDict):
    """Represents a row for database insertion output."""

    id: str
    payload: str


class S3ObjectMetadata(TypedDict, total=False):
    """Metadata for writing to S3 (optional)."""

    bucket: str
    key: str
    region: str
    content_type: str
    tags: dict[str, str]


def validate_dict(data: dict[str, Any], required_keys: list[str]) -> bool:
    """Check that all required keys exist in a dictionary.

    Args:
        data (dict[str, Any]): Dictionary to validate.
        required_keys (list[str]): Required keys to check.

    Returns:
        bool: True if all required keys are present.

    """
    return all(key in data for key in required_keys)


def validate_list_of_dicts(data: Any, required_keys: list[str]) -> bool:
    """Validate that input is a list of dicts, each with required keys.

    Args:
        data (Any): Data to validate.
        required_keys (list[str]): Required keys for each dict.

    Returns:
        bool: True if input is valid list of valid dicts.

    """
    if not isinstance(data, list):
        return False
    return all(isinstance(item, dict) and validate_dict(item, required_keys) for item in data)


def is_valid_payload(data: Any) -> bool:
    """Perform basic validation for a single payload.

    Args:
        data (Any): Input data to check.

    Returns:
        bool: True if input is a dict with 'symbol' and 'timestamp'.

    """
    return isinstance(data, dict) and "symbol" in data and "timestamp" in data


def is_valid_batch(data: Any) -> bool:
    """Validate a batch of payloads.

    Args:
        data (Any): Input to validate.

    Returns:
        bool: True if input is a valid list of payloads.

    """
    return validate_list_of_dicts(data, ["symbol", "timestamp"])


def is_valid_trade_event(data: Any) -> bool:
    """Validate that input is a well-formed TradeEvent.

    Args:
        data (Any): Input data to check.

    Returns:
        bool: True if input is a valid trade event with required fields.

    """
    if not isinstance(data, dict):
        return False

    required_fields = ["symbol", "action", "quantity", "price", "timestamp"]
    if not all(field in data for field in required_fields):
        return False

    if data["action"] not in ("BUY", "SELL"):
        return False

    if not isinstance(data["quantity"], (int, float)):
        return False

    if not isinstance(data["price"], (int, float)):
        return False

    return True
