"""Validate stock data to ensure it conforms to the required schema.

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
    """Validates the data to ensure it conforms to the required schema.
    
    The function checks that the input data is a dictionary containing
    the required keys: 'symbol', 'price', 'volume', and 'timestamp'.
    It also validates the individual fields using helper functions.

    :param data: The data to validate.
    :type data: dict[str
    :param data: dict[str:
    :param Any: returns: True if data is valid, False otherwise.
    :param data: dict[str:
    :param Any: returns: True if data is valid, False otherwise.
    :param data: dict[str:
    :param Any: returns: True if data is valid, False otherwise.
    :param data: 
    :type data: dict[str :
    :param Any]: 
    :param data: 
    :type data: dict[str :
    :param data: dict[str: 
    :returns: True if data is valid, False otherwise.
    :rtype: bool
    :raises TypeError: If the data is not a dictionary.

    Notes
    -----
    TypeError
        If the data is not a dictionary.
    Notes
    -----
        The function logs an error message for each validation failure.
    """
    # Define the set of required keys
    required_keys: set[str] = {"symbol", "price", "volume", "timestamp"}

    if not isinstance(data, dict):
        # Data must be a dictionary
        logger.error("Invalid data type. Expected a dictionary.")
        raise TypeError("Data must be a dictionary.")

    # Check that all required keys are present
    missing_keys: set[str] = required_keys - data.keys()
    if missing_keys:
        logger.error(f"Missing required keys in data: {missing_keys}")
        return False

    # Check that none of the required keys have null values
    for key in required_keys:
        if data.get(key) is None:
            logger.error(f"Null value for required key: {key}")
            return False

    # Validate individual fields
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

    # If all validations pass, return True
    return True


def _validate_symbol(symbol: str) -> bool:
    """Validates the 'symbol' field to ensure it is a string of alphabetical characters.

    :param symbol: The value of the 'symbol' field.
    :type symbol: str
    :param symbol: str:
    :param symbol: str:
    :param symbol: str:
    :param symbol: 
    :type symbol: str :
    :param symbol: 
    :type symbol: str :
    :param symbol: str: 
    :returns: True if valid, False otherwise.
    :rtype: bool

    Notes
    -----
    """
    if not isinstance(symbol, str) or not symbol.isalpha():
        logger.error(f"Invalid symbol format: {symbol}")
        return False
    return True


def _validate_price(price: Any) -> bool:
    """Validates the 'price' field to ensure it is a non-negative number.

    :param price: The value of the 'price' field.
    :type price: Any
    :param price: Any:
    :param price: Any:
    :param price: Any:
    :param price: 
    :type price: Any :
    :param price: 
    :type price: Any :
    :param price: Any: 
    :returns: True if valid, False otherwise.
    :rtype: bool

    Notes
    -----
    """
    # Check if the price is an integer or float and if it is non-negative
    if not isinstance(price, (int, float)) or price < 0:
        logger.error(f"Invalid price: {price}")  # Log an error if validation fails
        return False
    return True  # Return True if the price is valid


def _validate_volume(volume: Any) -> bool:
    """Validates the 'volume' field to ensure it is a non-negative integer.
    
    Args:
    ----
        volume (Any): The value of the 'volume' field.

    :param volume: Any:
    :param volume: Any:
    :param volume: Any:
    :param volume: 
    :type volume: Any :
    :param volume: 
    :type volume: Any :
    :param volume: Any: 

    Notes
    -----
        A non-negative integer is used to represent the volume of a stock quote.
        The function checks that the provided volume is of type int and if it
        is non-negative. If the validation fails, an error message is logged.
    """
    if not isinstance(volume, int) or volume < 0:
        logger.error(f"Invalid volume format: {volume}")
        return False
    return True


def _validate_timestamp(timestamp: Any) -> bool:
    """Validates the 'timestamp' field to ensure it is a string.
    
    The function checks that the provided timestamp is of type string.
    It logs an error if the validation fails.
    
    Args:
    ----
        timestamp (Any): The value of the 'timestamp' field.

    :param timestamp: Any:
    :param timestamp: Any:
    :param timestamp: Any:
    :param timestamp: 
    :type timestamp: Any :
    :param timestamp: 
    :type timestamp: Any :
    :param timestamp: Any: 

    
    """
    # Ensure the timestamp is a string
    if not isinstance(timestamp, str):
        logger.error(f"Invalid timestamp format: {timestamp}")  # Log an error if validation fails
        return False
    return True  # Return True if the timestamp is valid
