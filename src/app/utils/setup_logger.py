"""
Configure and return a logger for the application.

This module provides a function to configure and return a logger instance with a
specified name and logging level.
"""

import logging


def setup_logger(name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger for the application.

    Logs messages to the console using a StreamHandler and a specified format.
    If the logger already exists, it reuses the existing instance.

    Args:
    ----
        name (Optional[str]): Name of the logger. Defaults to "poller" if not specified.
        level (int): Logging level to use. Defaults to logging.INFO.

    Returns:
    -------
        logging.Logger: Configured logger instance.
    """
    logger_name = name or "poller"
    logger = logging.getLogger(logger_name)

    if not logger.hasHandlers():
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Module-level logger
logger = setup_logger(level=logging.DEBUG)
