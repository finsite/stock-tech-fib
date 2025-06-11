"""Shared configuration module for all polling services.

Provides typed, cached getter functions to retrieve configuration values
from Vault, environment variables, or defaults — in that order.
"""

import os
from functools import lru_cache

from app.utils.types import OutputMode
from app.utils.vault_client import VaultClient, get_secret_or_env

_vault = VaultClient()


@lru_cache
def get_config_value(key: str, default: str | None = None) -> str:
    """Retrieve a configuration value from Vault, environment, or fallback.

    Args:
        key: The configuration key to retrieve.
        default: Fallback value if the key is missing.

    Returns:
        The resolved configuration value.

    Raises:
        ValueError: If no value is found and no default is provided.

    """
    val = _vault.get(key, os.getenv(key))
    if val is None:
        if default is not None:
            return str(default)
        raise ValueError(f"❌ Missing required config for key: {key}")
    return str(val)


@lru_cache
def get_config_bool(key: str, default: bool = False) -> bool:
    """Retrieve a boolean config value with support for various true/false
    strings.

    Args:
        key: The configuration key.
        default: Default boolean value.

    Returns:
        Parsed boolean from config string.

    """
    val = get_config_value(key, str(default)).strip().lower()
    return val in {"1", "true", "yes", "on"}


@lru_cache
def get_environment() -> str:
    """Return the current runtime environment (e.g., 'dev', 'prod')."""
    return get_config_value("ENVIRONMENT", "dev")


@lru_cache
def get_poller_name() -> str:
    """Return the unique poller name for identification."""
    return get_config_value("POLLER_NAME", "replace_me_poller_name")


@lru_cache
def get_polling_interval() -> int:
    """Return polling interval in seconds."""
    return int(get_config_value("POLLING_INTERVAL", "60"))


@lru_cache
def get_batch_size() -> int:
    """Return number of items to process per batch."""
    return int(get_config_value("BATCH_SIZE", "10"))


@lru_cache
def get_rate_limit() -> int:
    """Return allowed requests per second (0 = unlimited)."""
    return int(get_config_value("RATE_LIMIT", "0"))


@lru_cache
def get_output_mode() -> OutputMode:
    """Return configured output mode.

    Raises:
        ValueError: If the mode is invalid.

    """
    raw_value = get_config_value("OUTPUT_MODE", "queue").lower()
    try:
        return OutputMode(raw_value)
    except ValueError:
        raise ValueError(
            f"❌ Invalid OUTPUT_MODE: '{raw_value}'. Must be one of: {[m.value for m in OutputMode]}"
        )


@lru_cache
def get_queue_type() -> str:
    """Return the messaging queue backend in use (e.g., 'rabbitmq')."""
    return get_config_value("QUEUE_TYPE", "rabbitmq")


@lru_cache
def get_rabbitmq_host() -> str:
    """Return the hostname of RabbitMQ."""
    return get_config_value("RABBITMQ_HOST", "localhost")


@lru_cache
def get_rabbitmq_port() -> int:
    """Return the RabbitMQ port number."""
    return int(get_config_value("RABBITMQ_PORT", "5672"))


@lru_cache
def get_rabbitmq_vhost() -> str:
    """Return RabbitMQ virtual host."""
    vhost = get_config_value("RABBITMQ_VHOST")
    if not vhost:
        raise ValueError("❌ Missing required config: RABBITMQ_VHOST must be set.")
    return vhost


@lru_cache
def get_rabbitmq_user() -> str:
    """Return RabbitMQ username."""
    return get_config_value("RABBITMQ_USER", "")


@lru_cache
def get_rabbitmq_password() -> str:
    """Return RabbitMQ password."""
    return get_config_value("RABBITMQ_PASS", "")


@lru_cache
def get_rabbitmq_exchange() -> str:
    """Return RabbitMQ exchange name."""
    return get_config_value("RABBITMQ_EXCHANGE", "stock_data_exchange")


@lru_cache
def get_rabbitmq_routing_key() -> str:
    """Return RabbitMQ routing key."""
    return get_config_value("RABBITMQ_ROUTING_KEY", "stock_data")


@lru_cache
def get_rabbitmq_queue() -> str:
    """Return RabbitMQ queue name."""
    return get_config_value("RABBITMQ_QUEUE", "default_queue")


@lru_cache
def get_dlq_name() -> str:
    """Return RabbitMQ dead-letter queue name."""
    return get_config_value("DLQ_NAME", "default_dlq")


@lru_cache
def get_sqs_queue_url() -> str:
    """Return AWS SQS queue URL."""
    return get_config_value("SQS_QUEUE_URL", "")


@lru_cache
def get_sqs_region() -> str:
    """Return AWS region for SQS."""
    return get_config_value("SQS_REGION", "us-east-1")


@lru_cache
def get_log_level() -> str:
    """Return the application's log level."""
    return get_config_value("LOG_LEVEL", "INFO")


@lru_cache
def get_poller_type() -> str:
    """Return poller type for tagging (e.g., 'stock')."""
    return get_config_value("POLLER_TYPE", "stock")


@lru_cache
def get_retry_delay() -> int:
    """Return delay in seconds before retrying failed polls."""
    return int(get_config_value("RETRY_DELAY", "5"))


@lru_cache
def get_symbols() -> list[str]:
    """Return list of symbols to process from comma-separated string."""
    symbols = get_config_value("SYMBOLS", "")
    return [s.strip() for s in symbols.split(",") if s.strip()]


@lru_cache
def get_newsapi_key() -> str:
    """Return the NewsAPI key from config."""
    return get_config_value("NEWSAPI_KEY")


@lru_cache
def get_newsapi_rate_limit() -> tuple[int, int]:
    """Return NewsAPI rate limit as (rate, capacity)."""
    return (
        int(get_config_value("NEWSAPI_RATE", "5")),
        int(get_config_value("NEWSAPI_CAPACITY", "10")),
    )


@lru_cache
def get_newsapi_timeout() -> int:
    """Return the timeout value in seconds for NewsAPI requests."""
    return int(get_config_value("NEWSAPI_TIMEOUT", "10"))


@lru_cache
def get_youtube_api_key() -> str:
    """Return the YouTube API key from config."""
    return get_config_value("YOUTUBE_API_KEY")


@lru_cache
def get_reddit_client_id() -> str:
    """Return the Reddit client ID from config."""
    return get_config_value("REDDIT_CLIENT_ID")


@lru_cache
def get_reddit_client_secret() -> str:
    """Return the Reddit client secret from config."""
    return get_config_value("REDDIT_CLIENT_SECRET")


@lru_cache
def get_alpha_vantage_api_key() -> str:
    """Return the Alpha Vantage API key from secrets or environment."""
    return get_secret_or_env("ALPHA_VANTAGE_API_KEY")


@lru_cache
def get_alpha_vantage_fill_rate_limit() -> int:
    """Return the fill rate limit for Alpha Vantage polling."""
    return int(get_secret_or_env("ALPHA_VANTAGE_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_finnhub_api_key() -> str:
    """Return the Finnhub API key from secrets or environment."""
    return get_secret_or_env("FINNHUB_API_KEY")


@lru_cache
def get_finnhub_fill_rate_limit() -> int:
    """Return the fill rate limit for Finnhub polling."""
    return int(get_secret_or_env("FINNHUB_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_polygon_api_key() -> str:
    """Return the Polygon API key from secrets or environment."""
    return get_secret_or_env("POLYGON_API_KEY")


@lru_cache
def get_polygon_fill_rate_limit() -> int:
    """Return the fill rate limit for Polygon polling."""
    return int(get_secret_or_env("POLYGON_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_rapidapi_key() -> str:
    """Return the RapidAPI key from secrets or environment."""
    return get_secret_or_env("RAPIDAPI_KEY")


@lru_cache
def get_rapidapi_host() -> str:
    """Return the RapidAPI host for Yahoo Finance access."""
    return get_secret_or_env("RAPIDAPI_HOST", default="yahoo-finance15.p.rapidapi.com")


@lru_cache
def get_yfinance_fill_rate_limit() -> int:
    """Return the fill rate limit for yFinance polling."""
    return int(get_secret_or_env("YFINANCE_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_intrinio_key() -> str:
    """Return the Intrinio API key from secrets or environment."""
    return get_secret_or_env("INTRINIO_API_KEY")


@lru_cache
def get_intrinio_fill_rate_limit() -> int:
    """Return the fill rate limit for Intrinio polling."""
    return int(get_secret_or_env("INTRINIO_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_quandl_api_key() -> str:
    """Return the Quandl API key from secrets or environment."""
    return get_secret_or_env("QUANDL_API_KEY")


@lru_cache
def get_quandl_fill_rate_limit() -> int:
    """Return the fill rate limit for Quandl polling."""
    return int(get_secret_or_env("QUANDL_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_iex_api_key() -> str:
    """Return the IEX Cloud API key from secrets or environment."""
    return get_secret_or_env("IEX_API_KEY")


@lru_cache
def get_iex_fill_rate_limit() -> int:
    """Return the fill rate limit for IEX polling."""
    return int(get_secret_or_env("IEX_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_finnazon_key() -> str:
    """Return the Finnazon API key from secrets or environment."""
    return get_secret_or_env("FINNAZON_API_KEY")


@lru_cache
def get_finnazon_fill_rate_limit() -> int:
    """Return the fill rate limit for Finnazon polling."""
    return int(get_secret_or_env("FINNAZON_FILL_RATE_LIMIT", default="60"))
