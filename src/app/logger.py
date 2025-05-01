"""Module to handle logging for Ichimoku Analysis Service."""

import logging


def setup_logger(name: str = "ichimoku") -> logging.Logger:
    """
    Sets up a logger with a standard format and INFO level.

    Args:
    ----
        name (str): Name of the logger.

    Returns:
    -------
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
