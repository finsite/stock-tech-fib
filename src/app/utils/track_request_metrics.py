"""Tracks metrics for individual API requests.

This function logs the result of API request operations, including the
symbol, rate limit, and whether the request was successful or not.
"""

from app.utils.setup_logger import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)


def track_request_metrics(
    symbol: str,
    rate_limit: int,
    time_window: float,
    success: bool = True,
) -> None:
    """Tracks metrics for individual API requests.

    Logs the result of API request operations, including the symbol,
    rate limit, and whether the request was successful or not.

    :param symbol: The stock symbol for the request.
    :type symbol: str
    :param rate_limit: The number of allowed requests.
    :type rate_limit: int
    :param time_window: The rate limit window in seconds.
    :type time_window: float
    :param success: Whether the request was successful. Defaults to True.
    :type success: bool
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    :param symbol: type symbol: str :
    :param rate_limit: type rate_limit: int :
    :param time_window: type time_window: float :
    :param success: Default value = True)
    :type success: bool :
    :param symbol: type symbol: str :
    :param rate_limit: type rate_limit: int :
    :param time_window: type time_window: float :
    :param success: Default value = True)
    :type success: bool :
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    :param symbol: str:
    :param rate_limit: int:
    :param time_window: float:
    :param success: bool:  (Default value = True)
    """
    status = "success" if success else "failure"
    message = (
        f"Request for symbol '{symbol}' {status}. Rate limit: {rate_limit} req/{time_window}s."
    )

    if success:
        logger.info(message)
    else:
        logger.error(message)
