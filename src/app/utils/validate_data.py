"""Validate stock data to ensure it conforms to the required schema.

This module provides validation utilities for stock-related data.
It ensures dictionaries contain the required fields and valid formats
for 'symbol', 'price', 'volume', and 'timestamp'.
"""

from typing import Any

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def validate_data(data: dict[str, Any]) -> bool:
    """
    Validate input stock data against expected schema.

    Checks presence of required keys and validates each field.

    Args:
        data (dict[str, Any]): The stock data dictionary to validate.

    Returns:
        bool: True if data is valid, False otherwise.

    Raises:
        TypeError: If the input is not a dictionary.
    """
    required_keys: set[str] = {"symbol", "price", "volume", "timestamp"}

    if not isinstance(data, dict):
        logger.error("❌ Expected data to be a dictionary.")
        raise TypeError("Data must be a dictionary.")

    missing_keys = required_keys - data.keys()
    if missing_keys:
        logger.error("❌ Missing required keys: %s", missing_keys)
        return False

    for key in required_keys:
        if data.get(key) is None:
            logger.error("❌ Null value for required key: %s", key)
            return False

    try:
        if not _validate_symbol(data["symbol"]):
            return False
        if not _validate_price(data["price"]):
            return False
        if not _validate_volume(data["volume"]):
            return False
        if not _validate_timestamp(data["timestamp"]):
            return False
    except Exception as e:
        logger.exception("❌ Exception during validation: %s", e)
        return False

    return True


def validate_message_schema(message: Any) -> bool:
    """
    Validate a message for required structure: 'symbol', 'timestamp', and 'data' (dict).

    Args:
        message (Any): The message to validate.

    Returns:
        bool: True if valid structure, False otherwise.
    """
    if not isinstance(message, dict):
        logger.debug("Invalid message type: expected dict.")
        return False
    if not all(k in message for k in ("symbol", "timestamp", "data")):
        logger.debug("Message missing required keys.")
        return False
    if not isinstance(message["data"], dict):
        logger.debug("Message 'data' field is not a dict.")
        return False
    return True


def _validate_symbol(symbol: Any) -> bool:
    """
    Validate that the 'symbol' is a non-empty alphabetic string.

    Args:
        symbol (Any): The symbol value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(symbol, str) or not symbol.isalpha():
        logger.error("❌ Invalid symbol format: %s", symbol)
        return False
    return True


def _validate_price(price: Any) -> bool:
    """
    Validate that the 'price' is a non-negative number.

    Args:
        price (Any): The price value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(price, (int, float)) or price < 0:
        logger.error("❌ Invalid price: %s", price)
        return False
    return True


def _validate_volume(volume: Any) -> bool:
    """
    Validate that the 'volume' is a non-negative integer.

    Args:
        volume (Any): The volume value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(volume, int) or volume < 0:
        logger.error("❌ Invalid volume: %s", volume)
        return False
    return True


def _validate_timestamp(timestamp: Any) -> bool:
    """
    Validate that the 'timestamp' is a string.

    Args:
        timestamp (Any): The timestamp value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(timestamp, str):
        logger.error("❌ Invalid timestamp: %s", timestamp)
        return False
    return True
