"""Configure and return a logger for the application.

This module provides a function to configure and return a logger
instance with a specified name and logging level.
"""

import logging


def setup_logger(name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger for the application.
    
    Logs messages to the console using a StreamHandler and a specified format.
    If the logger already exists, it reuses the existing instance.
    
    Args:
    ----
        name (Optional[str]): Name of the logger. Defaults to "poller" if not specified.
        level (int): Logging level to use. Defaults to logging.INFO.
    
    Returns:
    -------
        logging.Logger: Configured logger instance.

    :param name: str | None:  (Default value = None)
    :param level: int:  (Default value = logging.INFO)

    
    """
    # Default logger name if not provided
    logger_name = name or "poller"

    # Get the logger instance
    logger = logging.getLogger(logger_name)

    # Check if logger already has handlers to avoid duplicate logs
    if not logger.hasHandlers():
        # Set the logging level
        logger.setLevel(level)

        # Create a StreamHandler to output logs to the console
        handler = logging.StreamHandler()

        # Define the log message format
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Set the formatter for the handler
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

    # Return the configured logger
    return logger


# Module-level logger
logger = setup_logger(level=logging.DEBUG)
