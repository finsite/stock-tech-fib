"""
Configuration module for queue consumer pollers.

Provides typed getter functions to retrieve configuration values from Vault,
environment variables, or defaults.
"""

import os

from app.utils.vault_client import VaultClient

# Initialize and cache Vault client
_vault = VaultClient()


def get_config_value(key: str, default: str | None = None) -> str:
    """Retrieve a configuration value from Vault, environment variable, or default.

    Args:
      key(str): Configuration key to fetch.
      default(Optional[str]): Fallback value if key is not found.
      key: str: 
      default: str | None:  (Default value = None)

    Returns:
      str: The resolved value.

    
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
