"""Configure and return a logger for the application.

Supports optional structured (JSON-style) logging for production
environments.
"""

import json
import logging


class StructuredFormatter(logging.Formatter):
    """Structured log formatter that outputs logs as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string."""
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "filename": record.filename,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        return json.dumps(log_record)


def setup_logger(
    name: str | None = None,
    level: int = logging.INFO,
    structured: bool = False,
) -> logging.Logger:
    """Configure and return a logger for the application.

    Args:
        name (Optional[str]): Name of the logger.
        level (int): Logging level (e.g., logging.INFO).
        structured (bool): Whether to use structured (JSON) logging.

    Returns:
        logging.Logger: A configured logger instance.

    """
    logger_name = name or "poller"
    logger = logging.getLogger(logger_name)

    if not logger.hasHandlers():
        logger.setLevel(level)
        handler = logging.StreamHandler()

        if structured:
            formatter = StructuredFormatter()
        else:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Default module-level logger (non-structured)
logger = setup_logger(level=logging.DEBUG)
