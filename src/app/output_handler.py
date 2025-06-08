"""Module to handle output of analysis results to the configured target.

Supports logging, stdout, queue publishing, and future extensibility
to REST, S3, or database sinks.
"""

import json
from typing import Any, cast

from app import config_shared
from app.queue_sender import publish_to_queue
from app.utils.setup_logger import setup_logger
from app.utils.types import OutputMode

logger = setup_logger(__name__)


def send_to_output(data: list[dict[str, Any]]) -> None:
    """Route processed output to the configured destination.

    Parameters
    ----------
    data : list[dict[str, Any]]
        A list of enriched messages to route.

    Raises
    ------
    Exception
        Any exceptions during output handling are caught and logged.

    """
    try:
        mode = cast(OutputMode, config_shared.get_output_mode())

        if mode == "log":
            _output_to_log(data)
        elif mode == "stdout":
            _output_to_stdout(data)
        elif mode == "queue":
            _output_to_queue(data)
        elif mode == "rest":
            _output_to_rest(data)
        elif mode == "s3":
            _output_to_s3(data)
        elif mode == "database":
            _output_to_database(data)
        else:
            logger.warning("⚠️ Unknown output mode: %s — defaulting to log.", mode)
            _output_to_log(data)
    except Exception as e:
        logger.error("❌ Failed to send output: %s", e)


def _output_to_log(data: list[dict[str, Any]]) -> None:
    """Log data to application logs."""
    for item in data:
        logger.info("📝 Processed message:\n%s", json.dumps(item, indent=4))


def _output_to_stdout(data: list[dict[str, Any]]) -> None:
    """Print data to stdout (e.g., console)."""
    for item in data:
        print(json.dumps(item, indent=4))


def _output_to_queue(data: list[dict[str, Any]]) -> None:
    """Publish processed data to RabbitMQ or SQS."""
    publish_to_queue(data)
    logger.info("✅ Output published to queue: %d message(s)", len(data))


def _output_to_rest(data: list[dict[str, Any]]) -> None:
    """Log stub message for REST output (not yet implemented)."""
    logger.warning("⚠️ Output mode 'rest' not yet implemented.")


def _output_to_s3(data: list[dict[str, Any]]) -> None:
    """Log stub message for S3 output (not yet implemented)."""
    logger.warning("⚠️ Output mode 's3' not yet implemented.")


def _output_to_database(data: list[dict[str, Any]]) -> None:
    """Log stub message for database output (not yet implemented)."""
    logger.warning("⚠️ Output mode 'database' not yet implemented.")
