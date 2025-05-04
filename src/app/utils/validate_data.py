"""
Validate stock data to ensure it conforms to the required schema.

The module provides a function to validate stock data dictionaries
containing the following required keys: 'symbol', 'price', 'volume',
and 'timestamp'. It also provides helper functions to validate the
individual fields.
"""

from typing import Any

from app.utils.setup_logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)


def validate_data(data: dict[str, Any]) -> bool:
    """
    Validates the data to ensure it conforms to the required schema.

    The function checks that the input data is a dictionary containing
    the required keys: 'symbol', 'price', 'volume', and 'timestamp'.
    It also validates the individual fields using helper functions.

    Args:
      data(dict[str, Any]): The data to validate.
      data: dict[str:
      Any]:

    Returns:
      bool: True if data is valid, False otherwise.

    Raises:
      TypeError: If the data is not a dictionary.

    Notes:
    -----
    The function logs an error message for each validation failure.
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
    """
    Validates the 'symbol' field to ensure it is a string of alphabetical characters.

    Args:
      symbol(str): The value of the 'symbol' field.
      symbol: str:

    Returns:
      bool: True if valid, False otherwise.

    Notes:
    -----
    The function checks the provided symbol to ensure it is a string and contains
    only alphabetical characters. The function logs an error message if the
    validation fails.
    """
    if not isinstance(symbol, str) or not symbol.isalpha():
        logger.error(f"Invalid symbol format: {symbol}")
        return False
    return True


def _validate_price(price: Any) -> bool:
    """
    Validates the 'price' field to ensure it is a non-negative number.

    Args:
      price(Any): The value of the 'price' field.
      price: Any:

    Returns:
      bool: True if valid, False otherwise.

    Notes:
    -----
        A non-negative number is used to represent the price of a stock quote.
        The function checks the provided price to ensure it is an integer or
        float and if it is non-negative. If the validation fails, an error
        message is logged.
    """
    # Check if the price is an integer or float and if it is non-negative
    if not isinstance(price, (int, float)) or price < 0:
        logger.error(f"Invalid price: {price}")  # Log an error if validation fails
        return False
    return True  # Return True if the price is valid


def _validate_volume(volume: Any) -> bool:
    """
    Validates the 'volume' field to ensure it is a non-negative integer.

    Args:
    ----
        volume (Any): The value of the 'volume' field.

    Returns:
    -------
        bool: True if valid, False otherwise.

    Notes:
    -----
        A non-negative integer is used to represent the volume of a stock quote.
        The function checks that the provided volume is of type int and if it
        is non-negative. If the validation fails, an error message is logged.

    Args:
      volume: Any:

    Returns:
    """
    if not isinstance(volume, int) or volume < 0:
        logger.error(f"Invalid volume format: {volume}")
        return False
    return True


def _validate_timestamp(timestamp: Any) -> bool:
    """
    Validates the 'timestamp' field to ensure it is a string.

    The function checks that the provided timestamp is of type string.
    It logs an error if the validation fails.

    Args:
    ----
        timestamp (Any): The value of the 'timestamp' field.

    Returns:
    -------
        bool: True if valid, False otherwise.

    Args:
      timestamp: Any:

    Returns:
    """
    # Ensure the timestamp is a string
    if not isinstance(timestamp, str):
        logger.error(f"Invalid timestamp format: {timestamp}")  # Log an error if validation fails
        return False
    return True  # Return True if the timestamp is valid
