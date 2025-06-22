"""Module to handle output of analysis results to the configured target.

Supports logging, stdout, queue publishing, and future extensibility to
REST, S3, or database sinks. Includes retry logic, validation, and
optional metrics integration.
"""

import json
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from app import config_shared
from app.queue_sender import publish_to_queue
from app.utils.setup_logger import setup_logger
from app.utils.types import OutputMode, validate_list_of_dicts

logger = setup_logger(__name__)


def send_to_output(data: list[dict[str, Any]]) -> None:
    """
    Route processed output to one or more configured destinations.

    Validates and dispatches messages to each enabled output mode.

    Args:
        data (list[dict[str, Any]]): A list of enriched messages to route.
    """
    try:
        validate_list_of_dicts(data, required_keys=["text"])

        # Use OUTPUT_MODES if defined, fallback to single OUTPUT_MODE
        modes = config_shared.get_output_modes()
        for mode_str in modes:
            try:
                mode = OutputMode(mode_str)
            except ValueError:
                logger.warning("⚠️ Unknown output mode: %s — skipping.", mode_str)
                continue

            if mode == OutputMode.LOG:
                _output_to_log(data)
            elif mode == OutputMode.STDOUT:
                _output_to_stdout(data)
            elif mode == OutputMode.QUEUE:
                _output_to_queue(data)
            elif mode == OutputMode.REST:
                _output_to_rest(data)
            elif mode == OutputMode.S3:
                _output_to_s3(data)
            elif mode == OutputMode.DATABASE:
                _output_to_database(data)
            else:
                logger.warning("⚠️ Unhandled output mode: %s", mode)

    except Exception as e:
        logger.error("❌ Failed to send output: %s", e)


def _output_to_log(data: list[dict[str, Any]]) -> None:
    """Log data to application logs.

    Args:
        data (list[dict[str, Any]]): List of dictionaries to log.

    """
    for item in data:
        logger.info("📝 Processed message:\n%s", json.dumps(item, indent=4))


def _output_to_stdout(data: list[dict[str, Any]]) -> None:
    """Print data to stdout (e.g., console).

    Args:
        data (list[dict[str, Any]]): List of dictionaries to print.

    """
    for item in data:
        print(json.dumps(item, indent=4))


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def _output_to_queue(data: list[dict[str, Any]]) -> None:
    """Publish processed data to RabbitMQ or SQS with retry logic.

    Args:
        data (list[dict[str, Any]]): List of dictionaries to publish.

    """
    publish_to_queue(data)
    logger.info("✅ Output published to queue: %d message(s)", len(data))
    record_metric("output_queue_success", len(data))


def _output_to_rest(data: list[dict[str, Any]]) -> None:
    """Send output to a REST endpoint (stub).

    Args:
        data (list[dict[str, Any]]): List of dictionaries to send.

    """
    logger.warning("⚠️ Output mode 'rest' not yet implemented.")
    record_metric("output_rest_skipped", len(data))


def _output_to_s3(data: list[dict[str, Any]]) -> None:
    """Send output to S3 (stub).

    Args:
        data (list[dict[str, Any]]): List of dictionaries to upload.

    """
    logger.warning("⚠️ Output mode 's3' not yet implemented.")
    record_metric("output_s3_skipped", len(data))


def _output_to_database(data: list[dict[str, Any]]) -> None:
    """Write output to a database (stub).

    Args:
        data (list[dict[str, Any]]): List of dictionaries to write.

    """
    logger.warning("⚠️ Output mode 'database' not yet implemented.")
    record_metric("output_db_skipped", len(data))


def record_metric(name: str, value: int) -> None:
    """Record a named metric (placeholder for Prometheus or CloudWatch
    integration).

    Args:
        name (str): Metric name.
        value (int): Metric value.

    """
    logger.debug("📊 Metric: %s = %d", name, value)
