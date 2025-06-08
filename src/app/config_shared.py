"""Configuration module for polling services.

Provides typed getter functions to retrieve configuration values from
Vault, environment variables, or defaults — in that order.
"""

import os

from app.utils.vault_client import VaultClient
from app.utils.types import OutputMode
from typing import cast

# Initialize and cache Vault client
_vault = VaultClient()


def get_config_value(key: str, default: str | None = None) -> str:
    """Retrieve a configuration value from Vault, environment variable, or default.

    Args:
        key (str): The configuration key to retrieve.
        default (Optional[str]): Fallback value if the key is missing.

    Returns:
        str: The resolved configuration value.

    Raises:
        ValueError: If the key is missing and no default is provided.

    """
    val = _vault.get(key, os.getenv(key))
    if val is None:
        if default is not None:
            return str(default)
        raise ValueError(f"❌ Missing required config for key: {key}")
    return str(val)


# ------------------------------------------------------------------------------
# 🌍 General Environment
# ------------------------------------------------------------------------------


def get_environment() -> str:
    """Return the current runtime environment (e.g., 'dev', 'prod')."""
    return get_config_value("ENVIRONMENT", "dev")


def get_poller_name() -> str:
    """Return the poller's name."""
    return get_config_value("POLLER_NAME", "stock_tech_ichimoku")


# ------------------------------------------------------------------------------
# 🔁 Polling and Runtime Behavior
# ------------------------------------------------------------------------------


def get_polling_interval() -> int:
    """Polling interval in seconds between data fetch cycles."""
    return int(get_config_value("POLLING_INTERVAL", "60"))


def get_batch_size() -> int:
    """Number of items or messages to process in each batch."""
    return int(get_config_value("BATCH_SIZE", "10"))


def get_rate_limit() -> int:
    """Maximum number of requests per second (0 = unlimited)."""
    return int(get_config_value("RATE_LIMIT", "0"))


def get_output_mode() -> OutputMode:
    """Output mode: 'queue', 'log', 'stdout', 'rest', 's3', or 'database'."""
    return cast(OutputMode, get_config_value("OUTPUT_MODE", "queue"))

# ------------------------------------------------------------------------------
# 📬 Queue Type
# ------------------------------------------------------------------------------


def get_queue_type() -> str:
    """Queue system in use: 'rabbitmq' or 'sqs'."""
    return get_config_value("QUEUE_TYPE", "rabbitmq")


# ------------------------------------------------------------------------------
# 🐇 RabbitMQ Configuration
# ------------------------------------------------------------------------------


def get_rabbitmq_host() -> str:
    """Hostname of the RabbitMQ broker."""
    return get_config_value("RABBITMQ_HOST", "localhost")


def get_rabbitmq_port() -> int:
    """Port number for RabbitMQ connection."""
    return int(get_config_value("RABBITMQ_PORT", "5672"))


def get_rabbitmq_vhost() -> str:
    """Virtual host used for RabbitMQ connection."""
    vhost = get_config_value("RABBITMQ_VHOST")
    if not vhost:
        raise ValueError("❌ Missing required config: RABBITMQ_VHOST must be set.")
    return vhost


def get_rabbitmq_user() -> str:
    """Username for RabbitMQ authentication."""
    return get_config_value("RABBITMQ_USER", "")


def get_rabbitmq_password() -> str:
    """Password for RabbitMQ authentication."""
    return get_config_value("RABBITMQ_PASS", "")


def get_rabbitmq_exchange() -> str:
    """Exchange name to publish to or consume from."""
    return get_config_value("RABBITMQ_EXCHANGE", "stock_data_exchange")


def get_rabbitmq_routing_key() -> str:
    """Routing key used for message delivery in RabbitMQ."""
    return get_config_value("RABBITMQ_ROUTING_KEY", "stock_data")


def get_rabbitmq_queue() -> str:
    """RabbitMQ queue name."""
    return get_config_value("RABBITMQ_QUEUE", "stock_tech_ichimoku_queue")


def get_dlq_name() -> str:
    """Dead-letter queue name."""
    return get_config_value("DLQ_NAME", "stock_tech_ichimoku_dlq")


# ------------------------------------------------------------------------------
# 📦 Amazon SQS Configuration
# ------------------------------------------------------------------------------


def get_sqs_queue_url() -> str:
    """Full URL of the SQS queue."""
    return get_config_value("SQS_QUEUE_URL", "")


def get_sqs_region() -> str:
    """AWS region of the SQS queue."""
    return get_config_value("SQS_REGION", "us-east-1")
