"""Main entry point for the service.

This script initializes logging, loads the queue consumer, and begins
consuming data using the configured processing callback.
"""

import os
import sys

# Add 'src/' to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import config_shared
from app.output_handler import send_to_output
from app.queue_handler import consume_messages
from app.utils.setup_logger import setup_logger

# Initialize the module-level logger with optional structured logging
logger = setup_logger(
    __name__,
    structured=config_shared.get_config_bool("STRUCTURED_LOGGING", False),
)


def main() -> None:
    """Start the data processing service.

    This function initializes the service by calling the queue consumer,
    which begins listening to RabbitMQ or SQS and processes data using
    the `send_to_output` callback.
    """
    logger.info("🚀 Starting processing service...")
    consume_messages(send_to_output)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("❌ Unhandled exception in main: %s", e)
        sys.exit(1)
