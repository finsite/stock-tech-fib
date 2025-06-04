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

    Args:
        symbol (str): The stock symbol for the request.
        rate_limit (int): The number of allowed requests.
        time_window (float): The rate limit window in seconds.
        success (bool): Whether the request was successful. Defaults to True.

    """
    status = "success" if success else "failure"
    message = (
        f"Request for symbol '{symbol}' {status}. Rate limit: {rate_limit} req/{time_window}s."
    )

    if success:
        logger.info(message)
    else:
        logger.error(message)
