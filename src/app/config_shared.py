"""Configuration module for polling services.

Provides typed getter functions to retrieve configuration values from
Vault, environment variables, or defaults — in that order.
"""

import os
from typing import cast

from app.utils.types import OutputMode, PollerType
from app.utils.vault_client import VaultClient, get_secret_or_env

# Initialize and cache Vault client
_vault = VaultClient()


def get_config_bool(key: str, default: bool = False) -> bool:
    """Retrieve a boolean config value with support for 'true', '1', 'yes', etc."""
    val = get_config_value(key, str(default)).strip().lower()
    return val in {"1", "true", "yes", "on"}


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


# --------------------------------------------------------------------------
# 🌍 General Environment
# --------------------------------------------------------------------------


def get_environment() -> str:
    """Return the current runtime environment (e.g., 'dev', 'prod')."""
    return get_config_value("ENVIRONMENT", "dev")


def get_poller_name() -> str:
    """Return the poller's name."""
    return get_config_value("POLLER_NAME", "replace_me_poller_name")


# --------------------------------------------------------------------------
# 🔁 Polling and Runtime Behavior
# --------------------------------------------------------------------------


def get_polling_interval() -> int:
    """Return polling interval in seconds between data fetch cycles."""
    return int(get_config_value("POLLING_INTERVAL", "60"))


def get_batch_size() -> int:
    """Return number of items or messages to process in each batch."""
    return int(get_config_value("BATCH_SIZE", "10"))


def get_rate_limit() -> int:
    """Return maximum number of requests per second (0 = unlimited)."""
    return int(get_config_value("RATE_LIMIT", "0"))


def get_output_mode() -> OutputMode:
    """Return output mode: 'queue', 'log', 'stdout', 'rest', 's3', or 'database'."""
    raw_value = get_config_value("OUTPUT_MODE", "queue").lower()
    try:
        return OutputMode(raw_value)
    except ValueError:
        raise ValueError(
            f"❌ Invalid OUTPUT_MODE: '{raw_value}'. Must be one of: {[m.value for m in OutputMode]}"
        )


# --------------------------------------------------------------------------
# 📬 Queue Type
# --------------------------------------------------------------------------


def get_queue_type() -> str:
    """Return queue system in use: 'rabbitmq' or 'sqs'."""
    return get_config_value("QUEUE_TYPE", "rabbitmq")


# --------------------------------------------------------------------------
# 🐇 RabbitMQ Configuration
# --------------------------------------------------------------------------


def get_rabbitmq_host() -> str:
    """Return hostname of the RabbitMQ broker."""
    return get_config_value("RABBITMQ_HOST", "localhost")


def get_rabbitmq_port() -> int:
    """Return port number for RabbitMQ connection."""
    return int(get_config_value("RABBITMQ_PORT", "5672"))


def get_rabbitmq_vhost() -> str:
    """Return virtual host used for RabbitMQ connection."""
    vhost = get_config_value("RABBITMQ_VHOST")
    if not vhost:
        raise ValueError("❌ Missing required config: RABBITMQ_VHOST must be set.")
    return vhost


def get_rabbitmq_user() -> str:
    """Return username for RabbitMQ authentication."""
    return get_config_value("RABBITMQ_USER", "")


def get_rabbitmq_password() -> str:
    """Return password for RabbitMQ authentication."""
    return get_config_value("RABBITMQ_PASS", "")


def get_rabbitmq_exchange() -> str:
    """Return exchange name to publish to or consume from."""
    return get_config_value("RABBITMQ_EXCHANGE", "stock_data_exchange")


def get_rabbitmq_routing_key() -> str:
    """Return routing key used for message delivery in RabbitMQ."""
    return get_config_value("RABBITMQ_ROUTING_KEY", "stock_data")


def get_rabbitmq_queue() -> str:
    """Return RabbitMQ queue name."""
    return get_config_value("RABBITMQ_QUEUE", "stock_tech_ichimoku_queue")


def get_dlq_name() -> str:
    """Return dead-letter queue name."""
    return get_config_value("DLQ_NAME", "stock_tech_ichimoku_dlq")


# --------------------------------------------------------------------------
# 📦 Amazon SQS Configuration
# --------------------------------------------------------------------------


def get_sqs_queue_url() -> str:
    """Return full URL of the SQS queue."""
    return get_config_value("SQS_QUEUE_URL", "")


def get_sqs_region() -> str:
    """Return AWS region of the SQS queue."""
    return get_config_value("SQS_REGION", "us-east-1")


# --------------------------------------------------------------------------
# 🔐 External API Keys
# --------------------------------------------------------------------------


def get_newsapi_key() -> str:
    """
    Returns the NewsAPI authentication key.

    This is required for accessing the NewsAPI endpoint.
    """
    return get_config_value("NEWSAPI_KEY")


def get_newsapi_rate_limit() -> tuple[int, int]:
    """
    Returns the NewsAPI rate limit configuration.

    Provides the request fill rate and burst capacity for rate limiting.
    These values are used by a token bucket or leaky bucket rate limiter.
    """
    return int(get_config_value("NEWSAPI_RATE", "5")), int(
        get_config_value("NEWSAPI_CAPACITY", "10")
    )


def get_newsapi_timeout() -> int:
    """
    Returns the timeout for NewsAPI requests.

    This controls the maximum time in seconds to wait for a response.
    """
    return int(get_config_value("NEWSAPI_TIMEOUT", "10"))


def get_youtube_api_key() -> str:
    """Returns the API key for accessing the YouTube Data API."""
    return get_config_value("YOUTUBE_API_KEY")


def get_reddit_client_id() -> str:
    """Returns the Reddit application client ID used for API authentication."""
    return get_config_value("REDDIT_CLIENT_ID")


def get_reddit_client_secret() -> str:
    """Returns the Reddit application client secret used for API authentication."""
    return get_config_value("REDDIT_CLIENT_SECRET")


# --------------------------------------------------------------------------
# 🔧 Logging and Poller Type
# --------------------------------------------------------------------------


def get_log_level() -> str:
    """Log level for the application ('DEBUG', 'INFO', 'WARNING', 'ERROR')."""
    return get_config_value("LOG_LEVEL", "INFO")


def get_poller_type() -> str:
    """Identifies the type of poller: 'stock', 'sentiment', 'alt', etc."""
    return get_config_value("POLLER_TYPE", "stock")


# --------------------------------------------------------------------------
# 🔁 Retry Behavior
# --------------------------------------------------------------------------


def get_retry_delay() -> int:
    """Delay in seconds before retrying failed polling attempts."""
    return int(get_config_value("RETRY_DELAY", "5"))


# --------------------------------------------------------------------------
# 🎯 Symbol Selection
# --------------------------------------------------------------------------


def get_symbols() -> list[str]:
    """List of symbols to fetch data for, from comma-separated string."""
    symbols = get_config_value("SYMBOLS", "")
    return [s.strip() for s in symbols.split(",") if s.strip()]


# === Alpha Vantage ===
def get_alpha_vantage_api_key() -> str:
    """Returns the API key for Alpha Vantage from Vault or environment."""
    return get_secret_or_env("ALPHA_VANTAGE_API_KEY")


def get_alpha_vantage_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for Alpha Vantage."""
    return int(get_secret_or_env("ALPHA_VANTAGE_FILL_RATE_LIMIT", default="60"))


# === Finnhub ===
def get_finnhub_api_key() -> str:
    """Returns the API key for Finnhub from Vault or environment."""
    return get_secret_or_env("FINNHUB_API_KEY")


def get_finnhub_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for Finnhub."""
    return int(get_secret_or_env("FINNHUB_FILL_RATE_LIMIT", default="60"))


# === Polygon ===
def get_polygon_api_key() -> str:
    """Returns the API key for Polygon.io from Vault or environment."""
    return get_secret_or_env("POLYGON_API_KEY")


def get_polygon_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for Polygon.io."""
    return int(get_secret_or_env("POLYGON_FILL_RATE_LIMIT", default="60"))


# === Yahoo Finance via RapidAPI ===
def get_rapidapi_key() -> str:
    """Returns the RapidAPI key for Yahoo Finance API access."""
    return get_secret_or_env("RAPIDAPI_KEY")


def get_rapidapi_host() -> str:
    """Returns the RapidAPI host string for Yahoo Finance."""
    return get_secret_or_env("RAPIDAPI_HOST", default="yahoo-finance15.p.rapidapi.com")


def get_yfinance_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for Yahoo Finance via RapidAPI."""
    return int(get_secret_or_env("YFINANCE_FILL_RATE_LIMIT", default="60"))


# === Intrinio ===
def get_intrinio_key() -> str:
    """Returns the API key for Intrinio from Vault or environment."""
    return get_secret_or_env("INTRINIO_API_KEY")


def get_intrinio_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for Intrinio."""
    return int(get_secret_or_env("INTRINIO_FILL_RATE_LIMIT", default="60"))


# === Quandl ===
def get_quandl_api_key() -> str:
    """Returns the API key for Quandl from Vault or environment."""
    return get_secret_or_env("QUANDL_API_KEY")


def get_quandl_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for Quandl."""
    return int(get_secret_or_env("QUANDL_FILL_RATE_LIMIT", default="60"))


# === IEX Cloud ===
def get_iex_api_key() -> str:
    """Returns the API key for IEX Cloud from Vault or environment."""
    return get_secret_or_env("IEX_API_KEY")


def get_iex_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for IEX Cloud."""
    return int(get_secret_or_env("IEX_FILL_RATE_LIMIT", default="60"))


# === Finnazon ===
def get_finnazon_key() -> str:
    """Returns the API key for Finnazon from Vault or environment."""
    return get_secret_or_env("FINNAZON_API_KEY")


def get_finnazon_fill_rate_limit() -> int:
    """Returns the per-second fill rate limit for Finnazon."""
    return int(get_secret_or_env("FINNAZON_FILL_RATE_LIMIT", default="60"))
