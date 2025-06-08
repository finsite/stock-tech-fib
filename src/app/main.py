"""Main entry point for the service.

This script initializes logging, loads the queue consumer,
and begins consuming data using the configured processing callback.
"""

import os
import sys

# Add 'src/' to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.setup_logger import setup_logger
from app.queue_handler import consume_messages
from app.output_handler import send_to_output

# Initialize the module-level logger
logger = setup_logger(__name__)


def main() -> None:
    """Starts the data processing service.

    This function initializes the service by calling the queue consumer,
    which will begin listening to RabbitMQ or SQS and processing data
    using the `send_to_output` callback.
    """
    logger.info("🚀 Starting processing service...")
    consume_messages(send_to_output)


if __name__ == "__main__":
    main()
