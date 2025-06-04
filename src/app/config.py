"""Configuration module for queue consumer pollers.

Provides typed getter functions to retrieve configuration values from
Vault, environment variables, or defaults.
"""

import os

from app.utils.vault_client import VaultClient

# Initialize and cache Vault client
_vault = VaultClient()


def get_config_value(key: str, default: str | None = None) -> str:
    """Retrieve a configuration value from Vault, environment variable, or
    default.
    
    Args:
    ----
      key(str): Configuration key to fetch.
      default(Optional[str]): Fallback value if key is not found.
      key: str:
      default: str | None:  (Default value = None)
      key: str:
      default: str | None:  (Default value = None)

    :param key: str:
    :param default: str | None:  (Default value = None)
    :param key: str:
    :param default: str | None:  (Default value = None)
    :param key: str:
    :param default: str | None:  (Default value = None)
    :param key: type key: str :
    :param default: Default value = None)
    :type default: str | None :
    :param key: type key: str :
    :param default: Default value = None)
    :type default: str | None :
    :param key: str:
    :param default: str | None:  (Default value = None)
    :param key: str:
    :param default: str | None:  (Default value = None)
    :param key: str: 
    :param default: str | None:  (Default value = None)

    """
    val = _vault.get(key, os.getenv(key))
    if val is None:
        if default is not None:
            return str(default)
        raise ValueError(f"❌ Missing required config for key: {key}")
    return str(val)


# ------------------------------------------------------------------------------
# 📬 Queue Configuration
# ------------------------------------------------------------------------------


def get_queue_type() -> str:
    """ """
    return get_config_value("QUEUE_TYPE", "rabbitmq")


# RabbitMQ Configuration
def get_rabbitmq_host() -> str:
    """RabbitMQ hostname."""
    return get_config_value("RABBITMQ_HOST", "localhost")


def get_rabbitmq_port() -> int:
    """RabbitMQ port number."""
    return int(get_config_value("RABBITMQ_PORT", "5672"))


def get_rabbitmq_vhost() -> str:
    """RabbitMQ virtual host."""
    vhost = get_config_value("RABBITMQ_VHOST")
    if not vhost:
        raise ValueError("❌ Missing required config: RABBITMQ_VHOST must be set.")
    return vhost


def get_rabbitmq_user() -> str:
    """RabbitMQ username."""
    return get_config_value("RABBITMQ_USER", "")


def get_rabbitmq_password() -> str:
    """RabbitMQ password."""
    return get_config_value("RABBITMQ_PASS", "")


def get_rabbitmq_exchange() -> str:
    """RabbitMQ exchange name."""
    return get_config_value("RABBITMQ_EXCHANGE", "stock_data_exchange")


def get_rabbitmq_routing_key() -> str:
    """RabbitMQ routing key."""
    return get_config_value("RABBITMQ_ROUTING_KEY", "stock_data")


# SQS Configuration
def get_sqs_queue_url() -> str:
    """Amazon SQS queue URL."""
    return get_config_value("SQS_QUEUE_URL", "")


def get_rabbitmq_queue() -> str:
    """RabbitMQ queue name."""
    return get_config_value("RABBITMQ_QUEUE", "candlestick_queue")


def get_dlq_name() -> str:
    """Dead-letter queue name (if configured)."""
    return get_config_value("DLQ_NAME", "candlestick_dlq")


def get_polling_interval() -> int:
    """Polling interval (in seconds) between batch pulls."""
    return int(get_config_value("POLLING_INTERVAL", "60"))


def get_batch_size() -> int:
    """Batch size for message polling or processing."""
    return int(get_config_value("BATCH_SIZE", "100"))


def get_output_mode() -> str:
    """Output mode: 'queue' or 'log' (for dry runs)."""
    return get_config_value("OUTPUT_MODE", "queue")


def get_sqs_region() -> str:
    """AWS region for the SQS queue."""
    return get_config_value("SQS_REGION", "us-east-1")
