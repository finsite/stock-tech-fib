"""Validate stock data to ensure it conforms to the required schema.

This module provides a function to validate stock data dictionaries
containing the following required keys: 'symbol', 'price', 'volume',
and 'timestamp'. It also provides helper functions to validate the
individual fields.
"""

from typing import Any

from app.utils.setup_logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)


def validate_data(data: dict[str, Any]) -> bool:
    """Validate input data to ensure it conforms to the required schema.

    This function checks that the input data is a dictionary containing
    the required keys: 'symbol', 'price', 'volume', and 'timestamp'.
    It also validates the individual fields using helper functions.

    :param data: The data to validate.
    :returns: True if data is valid, False otherwise.
    :raises TypeError: If the data is not a dictionary.
    """
    required_keys: set[str] = {"symbol", "price", "volume", "timestamp"}

    if not isinstance(data, dict):
        logger.error("Invalid data type. Expected a dictionary.")
        raise TypeError("Data must be a dictionary.")

    missing_keys: set[str] = required_keys - data.keys()
    if missing_keys:
        logger.error(f"Missing required keys in data: {missing_keys}")
        return False

    for key in required_keys:
        if data.get(key) is None:
            logger.error(f"Null value for required key: {key}")
            return False

    try:
        if not _validate_symbol(data["symbol"]):
            logger.error("Symbol validation failed.")
            return False
        if not _validate_price(data["price"]):
            logger.error("Price validation failed.")
            return False
        if not _validate_volume(data["volume"]):
            logger.error("Volume validation failed.")
            return False
        if not _validate_timestamp(data["timestamp"]):
            logger.error("Timestamp validation failed.")
            return False
    except Exception as e:
        logger.error(f"Validation failed with exception: {e}")
        return False

    return True


def _validate_symbol(symbol: str) -> bool:
    """Validate that the 'symbol' field is a string of alphabetical characters.

    :param symbol: The value of the 'symbol' field.
    :returns: True if valid, False otherwise.
    """
    if not isinstance(symbol, str) or not symbol.isalpha():
        logger.error(f"Invalid symbol format: {symbol}")
        return False
    return True


def _validate_price(price: Any) -> bool:
    """Validate that the 'price' field is a non-negative number.

    :param price: The value of the 'price' field.
    :returns: True if valid, False otherwise.
    """
    if not isinstance(price, (int, float)) or price < 0:
        logger.error(f"Invalid price: {price}")
        return False
    return True


def _validate_volume(volume: Any) -> bool:
    """Validate that the 'volume' field is a non-negative integer.

    :param volume: The value of the 'volume' field.
    :returns: True if valid, False otherwise.
    """
    if not isinstance(volume, int) or volume < 0:
        logger.error(f"Invalid volume format: {volume}")
        return False
    return True


def _validate_timestamp(timestamp: Any) -> bool:
    """Validate that the 'timestamp' field is a string.

    :param timestamp: The value of the 'timestamp' field.
    :returns: True if valid, False otherwise.
    """
    if not isinstance(timestamp, str):
        logger.error(f"Invalid timestamp format: {timestamp}")
        return False
    return True
