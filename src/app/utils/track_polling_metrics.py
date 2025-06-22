"""Track and expose metrics for polling operations.

This module logs polling results and emits Prometheus metrics to monitor
success and failure rates per source and symbol.
"""

import re
from typing import Literal

from prometheus_client import Counter

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

# Prometheus metric
polling_result_counter = Counter(
    "polling_result_total",
    "Count of polling outcomes by source and symbol",
    ["status", "source", "symbol"],
)


def _sanitize_label(value: str) -> str:
    """Sanitize a label value for safe use in Prometheus.

    Args:
        value (str): Original label value.

    Returns:
        str: Sanitized label value.
    """
    return re.sub(r"[^\w\-:.]", "_", value)[:64]


def track_polling_metrics(
    status: Literal["success", "failure"],
    source: str,
    symbol: str,
) -> None:
    """Track and log polling results.

    Args:
        status (Literal["success", "failure"]): Polling outcome.
        source (str): Source of the poll (e.g., "price", "news").
        symbol (str): Asset symbol being polled.

    Raises:
        ValueError: If status is not "success" or "failure".
    """
    if status not in {"success", "failure"}:
        raise ValueError("Invalid status. Must be 'success' or 'failure'.")

    sanitized_source = _sanitize_label(source)
    sanitized_symbol = _sanitize_label(symbol)

    # Emit Prometheus metric
    polling_result_counter.labels(
        status=status,
        source=sanitized_source,
        symbol=sanitized_symbol,
    ).inc()

    # Log the result
    message = f"Polling {status} for symbol '{symbol}' from source '{source}'."
    if status == "success":
        logger.info(message)
    else:
        logger.error(message)
