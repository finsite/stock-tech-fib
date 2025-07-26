"""Wrapper around the standard logger that applies redaction and structured logging.

This ensures that sensitive fields are redacted and logs follow consistent formatting.
"""

import logging
import os
from typing import Any, Optional

from app.utils.redactor import redact_dict
from app.utils.setup_logger import setup_logger

# Controls whether to log full payloads (only in dev/test)
SAFE_LOG_FULL: bool = os.getenv("SAFE_LOG_FULL", "false").lower() == "true"
SAFE_LOG_STRUCTURED: bool = os.getenv("SAFE_LOG_STRUCTURED", "false").lower() == "true"

# Base logger instance
logger: logging.Logger = setup_logger(__name__, structured=SAFE_LOG_STRUCTURED)


def safe_info(message: str, data: Optional[dict[str, Any]] = None) -> None:
    """
    Logs an info-level message with optional sanitized payload metadata.

    Args:
        message (str): Human-readable log message.
        data (Optional[dict]): Dictionary payload to log. Only logs redacted metadata unless SAFE_LOG_FULL is enabled.
    """
    if data is None:
        logger.info(message)
        return

    payload_size = len(data) if SAFE_LOG_FULL else len(redact_dict(data))
    logger.info("%s | payload_size=%d", message, payload_size)


def safe_warning(message: str, data: Optional[dict[str, Any]] = None) -> None:
    """
    Logs a warning-level message with optional sanitized payload metadata.

    Args:
        message (str): Human-readable log message.
        data (Optional[dict]): Dictionary payload to log. Only logs redacted metadata unless SAFE_LOG_FULL is enabled.
    """
    if data is None:
        logger.warning(message)
        return

    payload_size = len(data) if SAFE_LOG_FULL else len(redact_dict(data))
    logger.warning("%s | payload_size=%d", message, payload_size)


def safe_error(message: str, data: Optional[dict[str, Any]] = None) -> None:
    """
    Logs an error-level message with optional sanitized payload metadata.

    Args:
        message (str): Human-readable log message.
        data (Optional[dict]): Dictionary payload to log. Only logs redacted metadata unless SAFE_LOG_FULL is enabled.
    """
    if data is None:
        logger.error(message)
        return

    payload_size = len(data) if SAFE_LOG_FULL else len(redact_dict(data))
    logger.error("%s | payload_size=%d", message, payload_size)


def safe_debug(message: str, data: Optional[dict[str, Any]] = None) -> None:
    """
    Logs a debug-level message with optional sanitized payload metadata.

    Args:
        message (str): Human-readable log message.
        data (Optional[dict]): Dictionary payload to log. Only logs redacted metadata unless SAFE_LOG_FULL is enabled.
    """
    if data is None:
        logger.debug(message)
        return

    payload_size = len(data) if SAFE_LOG_FULL else len(redact_dict(data))
    logger.debug("%s | payload_size=%d", message, payload_size)
