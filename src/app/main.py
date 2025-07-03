"""Main entry point for the service.

Initializes logging, sets up metrics, validates configuration, and
starts consuming messages using the configured output handler.
"""

import os
import sys
import traceback

from app import config_shared
from app.output_handler import output_handler
from app.queue_handler import consume_messages
from app.utils.metrics_server import start_metrics_server
from app.utils.setup_logger import setup_logger

# Add 'src/' to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Initialize structured or plain logger
logger = setup_logger(
    __name__,
    structured=config_shared.get_config_bool("STRUCTURED_LOGGING", False),
)

REDACT_LOGS = config_shared.get_config_bool("REDACT_SENSITIVE_LOGS", True)


def redact(value: str) -> str:
    """Redact sensitive values from logs if redaction is enabled.

    Args:
        value (str): The value to redact.

    Returns:
        str: Redacted or original string.

    """
    return "[REDACTED]" if REDACT_LOGS else value


def validate_output_config() -> None:
    """Validate that required config variables are present for selected output modes.

    Logs sanitized values for REST, S3, and database outputs to help with troubleshooting.
    """
    output_modes = config_shared.get_output_modes()
    logger.info("📤 Output modes enabled: %s", output_modes)

    if "rest" in output_modes:
        url = config_shared.get_rest_output_url()
        logger.info("🌐 REST output URL: %s", redact(url))

    if "s3" in output_modes:
        bucket = config_shared.get_s3_output_bucket()
        prefix = config_shared.get_s3_output_prefix()
        logger.info("🪣 S3 bucket: %s, prefix: %s", redact(bucket), redact(prefix))

    if "database" in output_modes:
        db_url = config_shared.get_database_output_url()
        insert_sql = config_shared.get_database_insert_sql()
        logger.info("🗄️ DB URL: %s", redact(db_url))
        logger.debug("📝 Insert SQL: %s", redact(insert_sql))


def main() -> None:
    """Start the data processing service.

    This function performs startup tasks and begins consuming messages
    from the configured queue using the output handler.
    """
    logger.info("🚀 Starting processing service...")

    start_metrics_server()
    validate_output_config()

    logger.info(
        "✅ Ready. Listening for messages on queue type: %s", config_shared.get_queue_type()
    )
    consume_messages(output_handler.send)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("❌ Unhandled exception: %s", redact(str(e)))
        traceback.print_exc()
        sys.exit(1)
