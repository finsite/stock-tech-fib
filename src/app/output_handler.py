"""
Module to handle output of analysis results to a chosen output target.

This implementation logs the result, prints it to stdout, and sends the data to RabbitMQ
or SQS.
"""

import json
from typing import Any

from app.logger import setup_logger
from app.queue_sender import publish_to_queue

# Initialize logger
logger = setup_logger(__name__)


def send_to_output(data: dict[str, Any]) -> None:
    """
    Outputs processed analysis results to the configured output system.

    This includes logging the result, printing to console, and
    sending to RabbitMQ or SQS.

    Args:
        data (dict[str, any]): The processed analysis result.
    """
    try:
        formatted_output: str = json.dumps(data, indent=4)

        # Log and print
        logger.info("Sending data to output:\n%s", formatted_output)
        print(formatted_output)

        # Send to queue
        publish_to_queue([data])

    except Exception as e:
        logger.error("Failed to send output: %s", e)
