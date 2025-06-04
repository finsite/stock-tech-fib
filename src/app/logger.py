import logging
import os


def setup_logger(name: str = "app") -> logging.Logger:
    """Sets up and returns a logger with the specified name.
    
    If a logger with the same name already exists, it is reused.
    Otherwise, a new logger is created and configured to log to stdout
    with the format:
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    The default log level is controlled via the LOG_LEVEL environment variable.
    
    Args:
    ----
        name (str): The name of the logger. Defaults to "app".

    :param name: str:  (Default value = "app")
    :param name: str:  (Default value = "app")
    :param name: str:  (Default value = "app")
    :param name: (Default value = "app")
    :type name: str :
    :param name: (Default value = "app")
    :type name: str :
    :param name: str:  (Default value = "app")

    
    """
    logger: logging.Logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        log_format = os.getenv("LOG_FORMAT", "plain").lower()

        if log_format == "json":
            formatter = logging.Formatter(
                '{"timestamp":"%(asctime)s","name":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
            )
        else:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

    return logger
