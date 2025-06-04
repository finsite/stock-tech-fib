"""Tracks metrics for polling operations.

This function logs the result of polling operations, including the
source of the data and the symbol being polled. It also raises a
ValueError if the status is not 'success' or 'failure'.
"""

from typing import Literal

from app.utils.setup_logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)


def track_polling_metrics(status: Literal["success", "failure"], source: str, symbol: str) -> None:
    """Tracks metrics for polling operations.

    Args:
        status: Whether the polling was a "success" or "failure".
        source: The source system of the poll (e.g., "news", "price").
        symbol: The stock or asset symbol being polled.

    """
    # Validate status
    if status not in {"success", "failure"}:
        raise ValueError("Invalid status. Must be 'success' or 'failure'.")

    # Construct the log message
    message = f"Polling {status} for symbol '{symbol}' from source '{source}'."

    # Log the result based on status
    if status == "success":
        logger.info(message)
    else:
        logger.error(message)
