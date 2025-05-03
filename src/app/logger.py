import logging


def setup_logger(name: str = "app") -> logging.Logger:
    """
    Sets up a logger with the specified name.

    If a logger with the same name already exists, it will be reused.
    Otherwise, a new logger will be created with the specified name.

    The logger will be configured to output messages to the console
    with the following format:
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    The log level will be set to INFO.

    Args:
        name (str): The name of the logger. Defaults to "app".

    Returns:
        logging.Logger: The configured logger.
    """
    logger: logging.Logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler: logging.StreamHandler = logging.StreamHandler()
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
