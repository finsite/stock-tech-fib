"""Track and expose metrics for polling and output operations.

This module logs polling and output results, and emits Prometheus metrics to monitor
success and failure rates by source, symbol, and event type.
"""

import re
from typing import Literal

from prometheus_client import Counter

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

# Prometheus metric for polling operations
polling_result_counter = Counter(
    "polling_result_total",
    "Count of polling outcomes by source and symbol",
    ["status", "source", "symbol"],
)

# Prometheus metric for output operations (e.g., paper trading, queues)
output_result_counter = Counter(
    "output_result_total",
    "Count of output results by event and symbol",
    ["event", "symbol"],
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

    polling_result_counter.labels(
        status=status,
        source=sanitized_source,
        symbol=sanitized_symbol,
    ).inc()

    message = f"Polling {status} for symbol '{symbol}' from source '{source}'."
    if status == "success":
        logger.info(message)
    else:
        logger.error(message)


def track_output_metrics(event: str, symbol: str) -> None:
    """Track and log output results.

    This includes paper trading, queue delivery, or future sinks.

    Args:
        event (str): Event label (e.g., "paper_trade_sent", "output_queue_success").
        symbol (str): Related asset symbol.

    """
    sanitized_event = _sanitize_label(event)
    sanitized_symbol = _sanitize_label(symbol)

    output_result_counter.labels(
        event=sanitized_event,
        symbol=sanitized_symbol,
    ).inc()

    logger.debug("📊 Output metric: %s for symbol %s", event, symbol)
