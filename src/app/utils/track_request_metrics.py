"""Track and expose metrics for individual API requests.

This module logs API request outcomes and emits Prometheus metrics for monitoring
success and failure counts by symbol and request window.
"""

import re
from typing import Literal

from prometheus_client import Counter

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

# Prometheus metric for API request outcomes
api_request_result_counter = Counter(
    "api_request_result_total",
    "Total number of API requests by symbol and status",
    ["status", "symbol"],
)


def _sanitize_label(value: str) -> str:
    """Sanitize a string for use as a Prometheus label.

    Args:
        value (str): Original label value.

    Returns:
        str: Safe label value for Prometheus.

    """
    return re.sub(r"[^\w\-:.]", "_", value)[:64]


def track_request_metrics(
    symbol: str,
    rate_limit: int,
    time_window: float,
    success: bool = True,
) -> None:
    """Track and log metrics for an API request outcome.

    Args:
        symbol (str): The stock or asset symbol being queried.
        rate_limit (int): Maximum number of requests allowed.
        time_window (float): Time window in seconds for the rate limit.
        success (bool): Whether the request was successful.

    """
    status: Literal["success", "failure"] = "success" if success else "failure"
    sanitized_symbol = _sanitize_label(symbol)

    # Emit Prometheus metric
    api_request_result_counter.labels(
        status=status,
        symbol=sanitized_symbol,
    ).inc()

    # Log the request outcome
    message = (
        f"API request for symbol '{symbol}' {status}. "
        f"Rate limit: {rate_limit} req/{time_window:.1f}s."
    )
    if success:
        logger.info(message)
    else:
        logger.error(message)
