"""Track and expose metrics for individual API requests.

This module logs API request outcomes and emits metrics for monitoring
success/failure by symbol and request window.
"""

import re
from prometheus_client import Counter

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

# Prometheus metric
api_request_result_counter = Counter(
    "api_request_result_total",
    "Total number of API requests by symbol and status",
    ["status", "symbol"],
)


def _sanitize_label(value: str) -> str:
    """Sanitize a string for use as a Prometheus label."""
    return re.sub(r"[^\w\-:.]", "_", value)[:64]


def track_request_metrics(
    symbol: str,
    rate_limit: int,
    time_window: float,
    success: bool = True,
) -> None:
    """Track and log metrics for an API request.

    Args:
        symbol (str): The stock or asset symbol requested.
        rate_limit (int): Number of allowed requests per time window.
        time_window (float): The request time window in seconds.
        success (bool): Whether the request succeeded (default: True).
    """
    status = "success" if success else "failure"
    sanitized_symbol = _sanitize_label(symbol)

    # Emit Prometheus metric
    api_request_result_counter.labels(
        status=status,
        symbol=sanitized_symbol,
    ).inc()

    message = (
        f"Request for symbol '{symbol}' {status}. "
        f"Rate limit: {rate_limit} req/{time_window:.1f}s."
    )

    if success:
        logger.info(message)
    else:
        logger.error(message)
