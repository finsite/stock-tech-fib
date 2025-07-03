import logging
import sys
from logging import Logger


def setup_logger(
    name: str | None = None,
    level: int = logging.INFO,
    structured: bool = False,
) -> Logger:
    """Configure and return a logger with optional redaction and structured logging.

    Args:
        name (Optional[str]): Logger name.
        level (int): Log level (e.g., logging.INFO).
        structured (bool): Enable structured (JSON) logging. (Not yet implemented)

    Returns:
        Logger: Configured logger instance.

    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # Delay import to avoid circular dependency
    try:
        from app import config_shared

        redact = config_shared.get_redact_sensitive_logs()
    except Exception:
        redact = False

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

    if redact:
        logger.info("🔒 Redaction of sensitive data is ENABLED")
    else:
        logger.info("🔓 Redaction of sensitive data is DISABLED")

    # NOTE: 'structured' is accepted but not yet implemented
    if structured:
        logger.warning("⚠️ Structured logging requested but not yet supported.")

    return logger
