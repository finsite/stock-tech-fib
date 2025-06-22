"""Configure and return a logger for the application.

Supports optional structured (JSON-style) logging for production
environments and redaction of sensitive fields.
"""

import json
import logging
import re
from typing import Optional

from app import config_shared


class StructuredFormatter(logging.Formatter):
    """
    Structured log formatter that outputs logs as JSON strings.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as a JSON string.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: A JSON-formatted string of log fields.
        """
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


class RedactFilter(logging.Filter):
    """
    Logging filter that redacts sensitive information from log messages.
    """

    SENSITIVE_KEYS = {"api_key", "apikey", "token", "secret", "password", "auth"}

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter the log record, redacting sensitive values in the message.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            bool: Always True to allow the record after modification.
        """
        message = record.getMessage()

        for key in self.SENSITIVE_KEYS:
            # Match key=value and "key": "value" formats
            patterns = [
                re.compile(rf"({key}\s*=\s*)(\S+)", re.IGNORECASE),
                re.compile(rf'("{key}"\s*:\s*")([^"]+)(")', re.IGNORECASE),
            ]
            for pattern in patterns:
                message = pattern.sub(
                    lambda m: f"{m.group(1)}***{m.group(3) if m.lastindex and m.lastindex >= 3 else ''}",
                    message,
                )

        record.msg = message
        return True


def setup_logger(
    name: Optional[str] = None,
    level: int = logging.INFO,
    structured: bool = False,
    redact_sensitive: Optional[bool] = None,
) -> logging.Logger:
    """
    Configure and return a logger for the application.

    Args:
        name (Optional[str]): Name of the logger.
        level (int): Logging level (e.g., logging.INFO).
        structured (bool): Whether to use structured (JSON) logging.
        redact_sensitive (Optional[bool]): Override redaction setting (defaults to config).

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger_name = name or "poller"
    logger = logging.getLogger(logger_name)

    if not logger.hasHandlers():
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter: logging.Formatter = (
            StructuredFormatter()
            if structured
            else logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        handler.setFormatter(formatter)

        # Determine redaction setting
        enable_redaction = (
            redact_sensitive
            if redact_sensitive is not None
            else config_shared.get_redact_sensitive_logs()
        )
        if enable_redaction:
            handler.addFilter(RedactFilter())
            logger.debug("🔐 Log redaction enabled")

        logger.addHandler(handler)

    return logger


# Default logger instance for modules
logger = setup_logger(level=logging.DEBUG)
