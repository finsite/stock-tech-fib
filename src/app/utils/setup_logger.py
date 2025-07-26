"""Configures and returns a logger with console, optional file, and optional JSON output.
Supports redaction toggle from config_shared and multi-handler output.
"""

import logging
import sys
from logging import Logger
from logging.handlers import RotatingFileHandler

try:
    from pythonjsonlogger.json import JsonFormatter
except ImportError:
    JsonFormatter = None  # JSON logging fallback

from app import config_shared


def setup_logger(
    name: str | None = None,
    level: int | None = None,
    structured: bool | None = None,
    log_file: str | None = None,
) -> Logger:
    """Configure and return a logger with optional structured and file output.

    Args:
        name (Optional[str]): Logger name.
        level (Optional[int]): Logging level (overrides LOG_LEVEL config).
        structured (Optional[bool]): Use structured (JSON) logging (overrides LOG_FORMAT config).
        log_file (Optional[str]): Path to a log file (enables rotation if set).

    Returns:
        Logger: Configured logger instance.

    """
    logger = logging.getLogger(name or "app")

    if logger.hasHandlers():
        return logger

    # Resolve redaction
    redact_enabled = config_shared.get_redact_sensitive_logs()

    # Resolve level
    level_name = config_shared.get_log_level()
    resolved_level: int = level if level is not None else getattr(logging, level_name, logging.INFO)

    # Resolve structured format
    structured = structured if structured is not None else config_shared.get_log_format() == "json"

    # Choose formatter
    if structured and JsonFormatter:
        formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Console handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Optional rotating file handler
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(resolved_level)
    logger.propagate = False

    if redact_enabled:
        logger.info("🔒 Redaction of sensitive data is ENABLED")
    else:
        logger.info("🔓 Redaction of sensitive data is DISABLED")

    if structured and not JsonFormatter:
        logger.warning("⚠️ Structured logging requested but 'python-json-logger' is not installed.")

    return logger
