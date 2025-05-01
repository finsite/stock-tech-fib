"""
Main entry point of the application.

This script is responsible for starting the Fibonacci Analysis Service.

Imports:
    os: Provides a portable way of using operating system dependent functionality.
    sys: Provides access to system-specific parameters and functions.
    consume_messages: Function to start consuming messages from the configured queue.
    setup_logger: Function to initialize the logging configuration.

Attributes
----------
    logger (logging.Logger): Configured logger for the application.
"""

import os
import sys

# Add 'src/' to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.logger import setup_logger
from app.queue_handler import consume_messages

# Initialize logger
logger = setup_logger(__name__)


def main() -> None:
    """
    Main entry point of the application.

    This function starts the Fibonacci Analysis Service by consuming
    messages from the configured message queue. It logs the start of the
    service and invokes the `consume_messages` function to begin processing
    messages.
    """
    logger.info("Starting Fibonacci Analysis Service...")
    consume_messages()


if __name__ == "__main__":
    main()
