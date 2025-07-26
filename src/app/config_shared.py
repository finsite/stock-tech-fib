"""Shared configuration module for all polling services.

Provides typed, cached getter functions to retrieve configuration values
from Vault, environment variables, or defaults — in that order.
"""

from functools import lru_cache

from app.utils.config_utils import get_config_bool
from app.utils.types import OutputMode
from app.utils.vault_client import get_config_value_cached


@lru_cache
def get_environment() -> str:
    """Retrieve the runtime environment.

    Returns:
        str: The environment name (e.g., 'dev', 'staging', 'prod').

    Defaults to 'dev' if not set.

    """
    return get_config_value_cached("ENVIRONMENT", "dev")


@lru_cache
def get_poller_name() -> str:
    """Retrieve the unique name identifying this poller.

    Returns:
        str: Poller name used in logs and queue bindings.

    Defaults to 'replace_me_poller_name' if not set.

    """
    return get_config_value_cached("POLLER_NAME", "replace_me_poller_name")


@lru_cache
def get_polling_interval() -> int:
    """Retrieve the interval in seconds between polling operations.

    Returns:
        int: Number of seconds between poll cycles.

    Defaults to 60 if not set.

    """
    return int(get_config_value_cached("POLLING_INTERVAL", "60"))


@lru_cache
def get_batch_size() -> int:
    """Retrieve the number of items to process in a single batch.

    Returns:
        int: Batch size for processing messages.

    Defaults to 10 if not set.

    """
    return int(get_config_value_cached("BATCH_SIZE", "10"))


@lru_cache
def get_rate_limit() -> int:
    """Retrieve the rate limit in requests per second.

    Returns:
        int: Requests per second (0 = unlimited).

    Defaults to 0 if not set.

    """
    return int(get_config_value_cached("RATE_LIMIT", "0"))


@lru_cache
def get_output_mode() -> OutputMode:
    """Retrieve the configured output mode (e.g., 'queue', 'db', 's3').

    Returns:
        OutputMode: Enum representing the output mode.

    Raises:
        ValueError: If the mode is not a valid OutputMode.

    Defaults to 'queue' if not set.

    """
    raw_value = get_config_value_cached("OUTPUT_MODE", "queue").lower()
    try:
        return OutputMode(raw_value)
    except ValueError:
        raise ValueError(
            f"Invalid OUTPUT_MODE: '{raw_value}'. Must be one of: {[m.value for m in OutputMode]}"
        )


@lru_cache
def get_queue_type() -> str:
    """Retrieve the type of message queue in use.

    Returns:
        str: Queue type (e.g., 'rabbitmq', 'sqs').

    Defaults to 'rabbitmq' if not set.

    """
    return get_config_value_cached("QUEUE_TYPE", "rabbitmq")


@lru_cache
def get_rabbitmq_host() -> str:
    """Retrieve the hostname of the RabbitMQ broker.

    Returns:
        str: Hostname of the RabbitMQ server.

    Defaults to 'localhost' if not set.

    """
    return get_config_value_cached("RABBITMQ_HOST", "localhost")


@lru_cache
def get_rabbitmq_port() -> int:
    """Retrieve the port number for RabbitMQ.

    Returns:
        int: Port used to connect to RabbitMQ.

    Defaults to 5672 if not set.

    """
    return int(get_config_value_cached("RABBITMQ_PORT", "5672"))


@lru_cache
def get_rabbitmq_vhost() -> str:
    """Retrieve the RabbitMQ virtual host.

    Returns:
        str: Virtual host name.

    Raises:
        ValueError: If RABBITMQ_VHOST is not configured.

    """
    vhost = get_config_value_cached("RABBITMQ_VHOST")
    if not vhost:
        raise ValueError("Missing required config: RABBITMQ_VHOST must be set.")
    return vhost


@lru_cache
def get_rabbitmq_user() -> str:
    """Retrieve the RabbitMQ username.

    Returns:
        str: Username for authenticating to RabbitMQ.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("RABBITMQ_USER", "")


@lru_cache
def get_rabbitmq_password() -> str:
    """Retrieve the RabbitMQ password.

    Returns:
        str: Password for authenticating to RabbitMQ.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("RABBITMQ_PASS", "")


@lru_cache
def get_rabbitmq_exchange() -> str:
    """Retrieve the RabbitMQ exchange name.

    Returns:
        str: Exchange name to publish/subscribe to.

    Defaults to 'stock_data_exchange' if not set.

    """
    return get_config_value_cached("RABBITMQ_EXCHANGE", "stock_data_exchange")


@lru_cache
def get_rabbitmq_routing_key() -> str:
    """Retrieve the RabbitMQ routing key.

    Returns:
        str: Routing key for message publishing.

    Defaults to 'stock_data' if not set.

    """
    return get_config_value_cached("RABBITMQ_ROUTING_KEY", "stock_data")


@lru_cache
def get_rabbitmq_queue() -> str:
    """Retrieve the name of the RabbitMQ queue to consume from.

    Returns:
        str: Queue name.

    Defaults to 'default_queue' if not set.

    """
    return get_config_value_cached("RABBITMQ_QUEUE", "default_queue")


@lru_cache
def get_dlq_name() -> str:
    """Retrieve the name of the Dead Letter Queue (DLQ) for failed messages.

    Returns:
        str: DLQ queue name.

    Defaults to 'default_dlq' if not set.

    """
    return get_config_value_cached("DLQ_NAME", "default_dlq")


@lru_cache
def get_sqs_queue_url() -> str:
    """Retrieve the AWS SQS queue URL.

    Returns:
        str: Full SQS queue URL.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("SQS_QUEUE_URL", "")


@lru_cache
def get_sqs_region() -> str:
    """Retrieve the AWS region for SQS operations.

    Returns:
        str: AWS region name.

    Defaults to 'us-east-1' if not set.

    """
    return get_config_value_cached("SQS_REGION", "us-east-1")


@lru_cache
def get_log_level() -> str:
    """Retrieve the application log level.

    Returns:
        str: Logging level (e.g., 'INFO', 'DEBUG').

    Defaults to 'INFO' if not set.

    """
    return get_config_value_cached("LOG_LEVEL", "INFO")


def get_log_format() -> str:
    """Returns the configured log format.

    Returns:
        str: 'json' or 'text' (default is 'text').

    """
    return get_config_value_cached("LOG_FORMAT", "text").lower()


@lru_cache
def get_poller_type() -> str:
    """Retrieve the type/category of this poller.

    Returns:
        str: Label identifying the poller type (e.g., 'stock', 'sentiment').

    Defaults to 'stock' if not set.

    """
    return get_config_value_cached("POLLER_TYPE", "stock")


@lru_cache
def get_retry_delay() -> int:
    """Retrieve the number of seconds to wait before retrying failed operations.

    Returns:
        int: Retry delay in seconds.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("RETRY_DELAY", "5"))


@lru_cache
def get_symbols() -> list[str]:
    """Retrieve a list of stock symbols to process.

    Returns:
        List[str]: Symbols parsed from comma-separated config.

    Defaults to empty list if not set.

    """
    symbols = get_config_value_cached("SYMBOLS", "")
    return [s.strip() for s in symbols.split(",") if s.strip()]


@lru_cache
def get_newsapi_rate_limit() -> tuple[int, int]:
    """Retrieve the NewsAPI rate limit settings.

    Returns:
        Tuple[int, int]: (requests per second, burst capacity).

    Defaults to (5, 10) if not set.

    """
    return (
        int(get_config_value_cached("NEWSAPI_RATE", "5")),
        int(get_config_value_cached("NEWSAPI_CAPACITY", "10")),
    )


@lru_cache
def get_newsapi_timeout() -> int:
    """Retrieve the timeout in seconds for NewsAPI requests.

    Returns:
        int: Timeout duration.

    Defaults to 10 if not set.

    """
    return int(get_config_value_cached("NEWSAPI_TIMEOUT", "10"))


# --- API Keys & Rate Limits ---


@lru_cache
def get_alpha_vantage_api_key() -> str:
    """Retrieve the Alpha Vantage API key.

    Returns:
        str: API key string.

    Raises:
        ValueError: If ALPHA_VANTAGE_API_KEY is not found.

    """
    return get_config_value_cached("ALPHA_VANTAGE_API_KEY")


@lru_cache
def get_alpha_vantage_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Alpha Vantage.

    Returns:
        int: Requests per minute.

    Defaults to 60 if not set.

    """
    return int(get_config_value_cached("ALPHA_VANTAGE_FILL_RATE_LIMIT", "60"))


@lru_cache
def get_barchart_api_key() -> str:
    """Retrieve the API key for Barchart.

    Returns:
        str: API key string.

    Raises:
        ValueError: If BARCHART_API_KEY is not found.

    """
    return get_config_value_cached("BARCHART_API_KEY")


@lru_cache
def get_barchart_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Barchart.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("BARCHART_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_benzinga_api_key() -> str:
    """Retrieve the API key for Benzinga.

    Returns:
        str: API key string.

    Raises:
        ValueError: If BENZINGA_API_KEY is not found.

    """
    return get_config_value_cached("BENZINGA_API_KEY")


@lru_cache
def get_benzinga_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Benzinga.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("BENZINGA_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_binance_api_key() -> str:
    """Retrieve the API key for Binance.

    Returns:
        str: API key string.

    Raises:
        ValueError: If BINANCE_API_KEY is not found.

    """
    return get_config_value_cached("BINANCE_API_KEY")


@lru_cache
def get_binance_api_secret() -> str:
    """Retrieve the API secret for Binance.

    Returns:
        str: API secret string.

    Raises:
        ValueError: If BINANCE_API_SECRET is not found.

    """
    return get_config_value_cached("BINANCE_API_SECRET")


@lru_cache
def get_coinapi_key() -> str:
    """Retrieve the API key for CoinAPI.

    Returns:
        str: API key string.

    Raises:
        ValueError: If COINAPI_KEY is not found.

    """
    return get_config_value_cached("COINAPI_KEY")


@lru_cache
def get_coinapi_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for CoinAPI.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("COINAPI_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_coingecko_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for CoinGecko.

    Returns:
        int: Requests per second.

    Defaults to 20 if not set.

    """
    return int(get_config_value_cached("COINGECKO_FILL_RATE_LIMIT", "20"))


@lru_cache
def get_coinmarketcap_api_key() -> str:
    """Retrieve the API key for CoinMarketCap.

    Returns:
        str: API key string.

    Raises:
        ValueError: If COINMARKETCAP_API_KEY is not found.

    """
    return get_config_value_cached("COINMARKETCAP_API_KEY")


@lru_cache
def get_coinmarketcap_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for CoinMarketCap.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("COINMARKETCAP_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_cryptocompare_api_key() -> str:
    """Retrieve the API key for CryptoCompare.

    Returns:
        str: API key string.

    Raises:
        ValueError: If CRYPTOCOMPARE_API_KEY is not found.

    """
    return get_config_value_cached("CRYPTOCOMPARE_API_KEY")


@lru_cache
def get_cryptocompare_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for CryptoCompare.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("CRYPTOCOMPARE_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_finnazon_api_key() -> str:
    """Retrieve the API key for Finnazon.

    Returns:
        str: API key string.

    Raises:
        ValueError: If FINNAZON_API_KEY is not found.

    """
    return get_config_value_cached("FINNAZON_API_KEY")


@lru_cache
def get_finnazon_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Finnazon.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("FINNAZON_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_finnhub_api_key() -> str:
    """Retrieve the API key for Finnhub.

    Returns:
        str: API key string.

    Raises:
        ValueError: If FINNHUB_API_KEY is not found.

    """
    return get_config_value_cached("FINNHUB_API_KEY")


@lru_cache
def get_finnhub_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Finnhub.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("FINNHUB_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_glassnode_api_key() -> str:
    """Retrieve the API key for Glassnode.

    Returns:
        str: API key string.

    Raises:
        ValueError: If GLASSNODE_API_KEY is not found.

    """
    return get_config_value_cached("GLASSNODE_API_KEY")


@lru_cache
def get_huobi_api_key() -> str:
    """Retrieve the API key for Huobi.

    Returns:
        str: API key string.

    Raises:
        ValueError: If HUOBI_API_KEY is not found.

    """
    return get_config_value_cached("HUOBI_API_KEY")


@lru_cache
def get_huobi_api_secret() -> str:
    """Retrieve the API secret for Huobi.

    Returns:
        str: API secret string.

    Raises:
        ValueError: If HUOBI_API_SECRET is not found.

    """
    return get_config_value_cached("HUOBI_API_SECRET")


@lru_cache
def get_iex_api_key() -> str:
    """Retrieve the API key for IEX Cloud.

    Returns:
        str: API key string.

    Raises:
        ValueError: If IEX_API_KEY is not found.

    """
    return get_config_value_cached("IEX_API_KEY")


@lru_cache
def get_iex_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for IEX.

    Returns:
        int: Requests per minute.

    Defaults to 60 if not set.

    """
    return int(get_config_value_cached("IEX_FILL_RATE_LIMIT", "60"))


@lru_cache
def get_intotheblock_api_key() -> str:
    """Retrieve the API key for IntoTheBlock.

    Returns:
        str: API key string.

    Raises:
        ValueError: If INTOTHEBLOCK_API_KEY is not found.

    """
    return get_config_value_cached("INTOTHEBLOCK_API_KEY")


@lru_cache
def get_intrinio_api_key() -> str:
    """Retrieve the API key for Intrinio.

    Returns:
        str: API key string.

    Raises:
        ValueError: If INTRINIO_API_KEY is not found.

    """
    return get_config_value_cached("INTRINIO_API_KEY")


@lru_cache
def get_intrinio_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Intrinio.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("INTRINIO_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_kaiko_api_key() -> str:
    """Retrieve the API key for Kaiko.

    Returns:
        str: API key string.

    Raises:
        ValueError: If KAIKO_API_KEY is not found.

    """
    return get_config_value_cached("KAIKO_API_KEY")


@lru_cache
def get_kraken_api_key() -> str:
    """Retrieve the API key for Kraken.

    Returns:
        str: API key string.

    Raises:
        ValueError: If KRAKEN_API_KEY is not found.

    """
    return get_config_value_cached("KRAKEN_API_KEY")


@lru_cache
def get_kraken_api_secret() -> str:
    """Retrieve the API secret for Kraken.

    Returns:
        str: API secret string.

    Raises:
        ValueError: If KRAKEN_API_SECRET is not found.

    """
    return get_config_value_cached("KRAKEN_API_SECRET")


@lru_cache
def get_messari_api_key() -> str:
    """Retrieve the API key for Messari.

    Returns:
        str: API key string.

    Raises:
        ValueError: If MESSARI_API_KEY is not found.

    """
    return get_config_value_cached("MESSARI_API_KEY")


@lru_cache
def get_morningstar_api_key() -> str:
    """Retrieve the API key for Morningstar.

    Returns:
        str: API key string.

    Raises:
        ValueError: If MORNINGSTAR_API_KEY is not found.

    """
    return get_config_value_cached("MORNINGSTAR_API_KEY")


@lru_cache
def get_morningstar_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Morningstar.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("MORNINGSTAR_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_newsapi_key() -> str:
    """Retrieve the API key for NewsAPI.

    Returns:
        str: API key string.

    Raises:
        ValueError: If NEWSAPI_KEY is not found.

    """
    return get_config_value_cached("NEWSAPI_KEY")


@lru_cache
def get_nomics_api_key() -> str:
    """Retrieve the API key for Nomics.

    Returns:
        str: API key string.

    Raises:
        ValueError: If NOMICS_API_KEY is not found.

    """
    return get_config_value_cached("NOMICS_API_KEY")


@lru_cache
def get_okx_api_key() -> str:
    """Retrieve the API key for OKX.

    Returns:
        str: API key string.

    Raises:
        ValueError: If OKX_API_KEY is not found.

    """
    return get_config_value_cached("OKX_API_KEY")


@lru_cache
def get_okx_api_secret() -> str:
    """Retrieve the API secret for OKX.

    Returns:
        str: API secret string.

    Raises:
        ValueError: If OKX_API_SECRET is not found.

    """
    return get_config_value_cached("OKX_API_SECRET")


@lru_cache
def get_okx_passphrase() -> str:
    """Retrieve the passphrase for OKX API access.

    Returns:
        str: Passphrase string.

    Raises:
        ValueError: If OKX_PASSPHRASE is not found.

    """
    return get_config_value_cached("OKX_PASSPHRASE")


@lru_cache
def get_polygon_api_key() -> str:
    """Retrieve the API key for Polygon.io.

    Returns:
        str: API key string.

    Raises:
        ValueError: If POLYGON_API_KEY is not found.

    """
    return get_config_value_cached("POLYGON_API_KEY")


@lru_cache
def get_polygon_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Polygon.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("POLYGON_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_quandl_api_key() -> str:
    """Retrieve the API key for Quandl.

    Returns:
        str: API key string.

    Raises:
        ValueError: If QUANDL_API_KEY is not found.

    """
    return get_config_value_cached("QUANDL_API_KEY")


@lru_cache
def get_quandl_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Quandl.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("QUANDL_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_rapidapi_key() -> str:
    """Retrieve the API key for RapidAPI.

    Returns:
        str: API key string.

    Raises:
        ValueError: If RAPIDAPI_KEY is not found.

    """
    return get_config_value_cached("RAPIDAPI_KEY")


@lru_cache
def get_rapidapi_host() -> str:
    """Retrieve the RapidAPI host header value.

    Returns:
        str: Host value used in API requests.

    Defaults to 'yahoo-finance15.p.rapidapi.com' if not set.

    """
    return get_config_value_cached("RAPIDAPI_HOST", "yahoo-finance15.p.rapidapi.com")


@lru_cache
def get_reddit_client_id() -> str:
    """Retrieve the Reddit API client ID.

    Returns:
        str: Reddit application client ID.

    Raises:
        ValueError: If REDDIT_CLIENT_ID is not found.

    """
    return get_config_value_cached("REDDIT_CLIENT_ID")


@lru_cache
def get_reddit_client_secret() -> str:
    """Retrieve the Reddit API client secret.

    Returns:
        str: Reddit application secret string.

    Raises:
        ValueError: If REDDIT_CLIENT_SECRET is not found.

    """
    return get_config_value_cached("REDDIT_CLIENT_SECRET")


@lru_cache
def get_seekingalpha_api_key() -> str:
    """Retrieve the API key for SeekingAlpha.

    Returns:
        str: API key string.

    Raises:
        ValueError: If SEEKINGALPHA_API_KEY is not found.

    """
    return get_config_value_cached("SEEKINGALPHA_API_KEY")


@lru_cache
def get_seekingalpha_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for SeekingAlpha.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("SEEKINGALPHA_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_sentimentinvestor_api_key() -> str:
    """Retrieve the API key for SentimentInvestor.

    Returns:
        str: API key string.

    Raises:
        ValueError: If SENTIMENTINVESTOR_API_KEY is not found.

    """
    return get_config_value_cached("SENTIMENTINVESTOR_API_KEY")


@lru_cache
def get_sentimentinvestor_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for SentimentInvestor.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("SENTIMENTINVESTOR_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_twelvedata_api_key() -> str:
    """Retrieve the API key for TwelveData.

    Returns:
        str: API key string.

    Raises:
        ValueError: If TWELVEDATA_API_KEY is not found.

    """
    return get_config_value_cached("TWELVEDATA_API_KEY")


@lru_cache
def get_twelvedata_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for TwelveData.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("TWELVEDATA_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_yfinance_fill_rate_limit() -> int:
    """Retrieve the fill rate limit for Yahoo Finance.

    Returns:
        int: Requests per minute.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("YFINANCE_FILL_RATE_LIMIT", "5"))


@lru_cache
def get_youtube_api_key() -> str:
    """Retrieve the YouTube Data API key.

    Returns:
        str: API key string.

    Raises:
        ValueError: If YOUTUBE_API_KEY is not found.

    """
    return get_config_value_cached("YOUTUBE_API_KEY")


# --- General Configuration ---


@lru_cache
def get_structured_logging() -> bool:
    """Retrieve whether structured (JSON) logging is enabled.

    Returns:
        bool: True if STRUCTURED_LOGGING is enabled, else False.

    Defaults to False if not set.

    """
    return get_config_bool("STRUCTURED_LOGGING", False)


@lru_cache
def get_redact_sensitive_logs() -> bool:
    """Retrieve whether sensitive fields should be redacted from logs.

    Returns:
        bool: True if REDACT_SENSITIVE_LOGS is enabled, else False.

    Defaults to True if not set.

    """
    return get_config_bool("REDACT_SENSITIVE_LOGS", True)


@lru_cache
def get_debug_mode() -> bool:
    """Retrieve whether the application is in debug mode.

    Returns:
        bool: True if DEBUG is enabled, else False.

    Defaults to False if not set.

    """
    return get_config_bool("DEBUG", False)


@lru_cache
def get_dry_run_mode() -> bool:
    """Retrieve whether dry-run mode is enabled.

    In dry-run mode, the app may skip sending data or executing irreversible actions.

    Returns:
        bool: True if DRY_RUN is enabled, else False.

    Defaults to False if not set.

    """
    return get_config_bool("DRY_RUN", False)


@lru_cache
def get_healthcheck_enabled() -> bool:
    """Retrieve whether healthchecks are enabled for this service.

    Returns:
        bool: True if HEALTHCHECK_ENABLED is enabled, else False.

    Defaults to True if not set.

    """
    return get_config_bool("HEALTHCHECK_ENABLED", True)


@lru_cache
def get_healthcheck_host() -> str:
    """Retrieve the host address for the healthcheck server.

    Returns:
        str: Host address.

    Defaults to '0.0.0.0' if not set.

    """
    return get_config_value_cached("HEALTHCHECK_HOST", "127.0.0.1")


@lru_cache
def get_healthcheck_port() -> int:
    """Retrieve the port for the healthcheck server.

    Returns:
        int: Port number.

    Defaults to 8081 if not set.

    """
    return int(get_config_value_cached("HEALTHCHECK_PORT", "8081"))


@lru_cache
def get_metrics_enabled() -> bool:
    """Retrieve whether Prometheus metrics are enabled.

    Returns:
        bool: True if METRICS_ENABLED is enabled, else False.

    Defaults to True if not set.

    """
    val = get_config_value_cached("METRICS_ENABLED", "true").lower()
    return val in ("1", "true", "yes")


@lru_cache
def get_metrics_bind_address() -> str:
    """Retrieve the bind address for Prometheus metrics endpoint.

    Returns:
        str: Bind address (e.g., '0.0.0.0').

    Defaults to '0.0.0.0' if not set.

    """
    return get_config_value_cached("METRICS_BIND_ADDRESS", "127.0.0.1")


@lru_cache
def get_metrics_port() -> int:
    """Retrieve the port for Prometheus metrics endpoint.

    Returns:
        int: Port number.

    Defaults to 8000 if not set.

    Raises:
        ValueError: If METRICS_PORT is not a valid integer.

    """
    port_str = get_config_value_cached("METRICS_PORT", "8000")
    try:
        return int(port_str)
    except ValueError:
        raise ValueError(f"Invalid METRICS_PORT value: '{port_str}' must be an integer.")


@lru_cache
def get_service_name() -> str:
    """Retrieve the human-readable name of this service.

    Returns:
        str: Service name.

    Defaults to the poller name if not set.

    """
    return get_config_value_cached("SERVICE_NAME", get_poller_name())


# --- Crypto Configuration ---


@lru_cache
def get_crypto_symbols() -> list[str]:
    """Retrieve a list of cryptocurrency symbols to poll (e.g., BTC, ETH).

    Returns:
        List[str]: Uppercased symbol strings.

    Defaults to empty list if not set.

    """
    symbols = get_config_value_cached("CRYPTO_SYMBOLS", "")
    return [s.strip().upper() for s in symbols.split(",") if s.strip()]


@lru_cache
def get_crypto_exchange() -> str:
    """Retrieve the exchange name used for crypto polling.

    Returns:
        str: Exchange name (e.g., 'binance').

    Defaults to 'binance' if not set.

    """
    return get_config_value_cached("CRYPTO_EXCHANGE", "binance")


@lru_cache
def get_crypto_network() -> str:
    """Retrieve the blockchain network used for data collection.

    Returns:
        str: Network name (e.g., 'ethereum').

    Defaults to 'ethereum' if not set.

    """
    return get_config_value_cached("CRYPTO_NETWORK", "ethereum")


@lru_cache
def get_crypto_data_source() -> str:
    """Retrieve the data provider name used for crypto polling.

    Returns:
        str: Provider name (e.g., 'coinmarketcap').

    Defaults to 'coinmarketcap' if not set.

    """
    return get_config_value_cached("CRYPTO_DATA_SOURCE", "coinmarketcap")


@lru_cache
def get_crypto_queue_name() -> str:
    """Retrieve the queue name to route crypto messages.

    Returns:
        str: Queue name.

    Defaults to 'crypto_data_queue' if not set.

    """
    return get_config_value_cached("CRYPTO_QUEUE_NAME", "crypto_data_queue")


@lru_cache
def get_crypto_polling_interval() -> int:
    """Retrieve the polling interval for crypto services.

    Returns:
        int: Polling interval in seconds.

    Defaults to the general polling interval if not set.

    """
    return int(get_config_value_cached("CRYPTO_POLLING_INTERVAL", str(get_polling_interval())))


@lru_cache
def get_crypto_retry_delay() -> int:
    """Retrieve the retry delay after a failed crypto API call.

    Returns:
        int: Delay in seconds.

    Defaults to 10 if not set.

    """
    return int(get_config_value_cached("CRYPTO_RETRY_DELAY", "10"))


@lru_cache
def get_crypto_rate_limit() -> int:
    """Retrieve the rate limit in requests per second for crypto APIs.

    Returns:
        int: Requests per second.

    Defaults to 5 if not set.

    """
    return int(get_config_value_cached("CRYPTO_RATE_LIMIT", "5"))


@lru_cache
def get_candle_granularity() -> str:
    """Retrieve the candlestick data granularity.

    Returns:
        str: Interval string (e.g., '1m', '5m').

    Defaults to '1m' if not set.

    """
    return get_config_value_cached("CANDLE_GRANULARITY", "1m")


@lru_cache
def get_lookback_period_minutes() -> int:
    """Retrieve the lookback window for historical data in minutes.

    Returns:
        int: Number of minutes.

    Defaults to 60 if not set.

    """
    return int(get_config_value_cached("LOOKBACK_PERIOD_MINUTES", "60"))


@lru_cache
def get_websocket_enabled() -> bool:
    """Retrieve whether WebSocket streaming is enabled.

    Returns:
        bool: True if WEBSOCKET_ENABLED is enabled, else False.

    Defaults to False if not set.

    """
    return get_config_bool("WEBSOCKET_ENABLED", False)


@lru_cache
def get_websocket_url() -> str:
    """Retrieve the WebSocket endpoint URL.

    Returns:
        str: URL string.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("WEBSOCKET_URL", "")


@lru_cache
def get_websocket_auth_token() -> str:
    """Retrieve the WebSocket authentication token.

    Returns:
        str: Auth token string.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("WEBSOCKET_AUTH_TOKEN", "")


# --- Paper Trading Configuration ---


@lru_cache
def get_paper_trading_enabled() -> bool:
    """Retrieve whether paper trading mode is enabled.

    Returns:
        bool: True if PAPER_TRADING_ENABLED is set to 'true', else False.

    Defaults to False if not set.

    """
    return get_config_value_cached("PAPER_TRADING_ENABLED", "false").lower() == "true"


@lru_cache
def get_paper_trading_account_id() -> str:
    """Retrieve the paper trading account ID.

    Returns:
        str: Account ID string.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("PAPER_TRADING_ACCOUNT_ID", "")


@lru_cache
def get_paper_trading_queue_name() -> str:
    """Retrieve the RabbitMQ queue name used for paper trades.

    Returns:
        str: Queue name.

    Defaults to 'trades.paper' if not set.

    """
    return get_config_value_cached("PAPER_TRADING_QUEUE_NAME", "trades.paper")


@lru_cache
def get_paper_trading_exchange() -> str:
    """Retrieve the RabbitMQ exchange name used for paper trades.

    Returns:
        str: Exchange name.

    Defaults to 'trades_exchange' if not set.

    """
    return get_config_value_cached("PAPER_TRADING_EXCHANGE", "trades_exchange")


@lru_cache
def get_paper_trading_database_enabled() -> bool:
    """Retrieve whether paper trades should be stored in a database.

    Returns:
        bool: True if PAPER_TRADING_DATABASE_ENABLED is set to 'true', else False.

    Defaults to False if not set.

    """
    return get_config_value_cached("PAPER_TRADING_DATABASE_ENABLED", "false").lower() == "true"


@lru_cache
def get_paper_trade_mode() -> str:
    """Retrieve the output mode used for paper trading dispatch.

    Returns:
        str: Mode (e.g., 'paper', 'rest', 's3').

    Defaults to 'paper' if not set.

    """
    return get_config_value_cached("PAPER_TRADE_MODE", "paper")


# --- Output Handler Configuration ---


@lru_cache
def get_rest_endpoint_url() -> str:
    """Retrieve the REST API endpoint URL for output.

    Returns:
        str: Fully qualified URL to the REST sink.

    Defaults to 'http://localhost:8000/api' if not set.

    """
    return get_config_value_cached("REST_ENDPOINT_URL", "http://localhost:8000/api")


@lru_cache
def get_rest_timeout() -> int:
    """Retrieve the timeout in seconds for REST API output.

    Returns:
        int: Timeout duration in seconds.

    Defaults to 10 if not set.

    """
    return int(get_config_value_cached("REST_TIMEOUT", "10"))


@lru_cache
def get_s3_bucket_name() -> str:
    """Retrieve the name of the S3 bucket used for output.

    Returns:
        str: Bucket name.

    Defaults to 'default-bucket' if not set.

    """
    return get_config_value_cached("S3_BUCKET_NAME", "default-bucket")


@lru_cache
def get_s3_region() -> str:
    """Retrieve the AWS region of the S3 bucket.

    Returns:
        str: AWS region string.

    Defaults to 'us-east-1' if not set.

    """
    return get_config_value_cached("S3_REGION", "us-east-1")


@lru_cache
def get_s3_object_prefix() -> str:
    """Retrieve the prefix (folder path) for S3 object storage.

    Returns:
        str: Prefix path within the bucket.

    Defaults to 'output/' if not set.

    """
    return get_config_value_cached("S3_OBJECT_PREFIX", "output/")


@lru_cache
def get_s3_output_bucket() -> str:
    """Retrieve the S3 bucket name used for output dispatch.

    Returns:
        str: Bucket name.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("S3_OUTPUT_BUCKET", "")


@lru_cache
def get_s3_output_region() -> str:
    """Retrieve the AWS region for the S3 output bucket.

    Returns:
        str: AWS region name.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("S3_OUTPUT_REGION", "")


@lru_cache
def get_s3_output_prefix() -> str:
    """Retrieve the S3 key prefix (folder path) for output storage.

    Returns:
        str: S3 object key prefix.

    Defaults to 'output/' if not set.

    """
    return get_config_value_cached("S3_OUTPUT_KEY_PREFIX", "output/")


@lru_cache
def get_database_connection_url() -> str:
    """Retrieve the database connection URL for output.

    Returns:
        str: SQLAlchemy-compatible DB connection string.

    Defaults to 'sqlite:///output.db' if not set.

    """
    return get_config_value_cached("DATABASE_URL", "sqlite:///output.db")


@lru_cache
def get_database_output_url() -> str:
    """Retrieve the SQLAlchemy-compatible connection string for output database.

    Returns:
        str: Database URL (e.g., 'postgresql://user:pass@host/db').

    Defaults to empty string if not set.

    """
    return get_config_value_cached("DATABASE_OUTPUT_URL", "")


@lru_cache
def get_database_insert_sql() -> str:
    """Retrieve the SQL insert statement template for database output.

    Returns:
        str: SQL insert query.

    Defaults to empty string if not set.

    """
    return get_config_value_cached("DATABASE_INSERT_SQL", "")


@lru_cache
def get_output_modes() -> list[str]:
    """Retrieve a list of enabled output modes.

    Returns:
        List[str]: Enabled output modes (e.g., 's3', 'rest', 'database').

    Defaults to empty list if not set.

    """
    modes = get_config_value_cached("OUTPUT_MODES", "")
    return [m.strip().lower() for m in modes.split(",") if m.strip()]


@lru_cache
def get_rest_output_url() -> str:
    """Retrieve the REST endpoint URL for output dispatch.

    Returns:
        str: Fully qualified REST API URL.

    Raises:
        ValueError: If REST_OUTPUT_URL is not found.

    """
    return get_config_value_cached("REST_OUTPUT_URL")
