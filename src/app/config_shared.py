"""Shared configuration module for all polling services.

Provides typed, cached getter functions to retrieve configuration values
from Vault, environment variables, or defaults — in that order.
"""

import os
from functools import lru_cache
from typing import Optional, Tuple, List

from app.utils.types import OutputMode
from app.utils.vault_client import VaultClient, get_secret_or_env

_vault = VaultClient()


@lru_cache
def get_config_value(key: str, default: Optional[str] = None) -> str:
    """
    Retrieve a configuration value from Vault, environment variable, or fallback.

    Args:
        key (str): The configuration key to retrieve.
        default (Optional[str]): Fallback value if the key is not found.

    Returns:
        str: The resolved configuration value.

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
    """
    Retrieve a boolean configuration value with support for multiple true-like values.

    Args:
        key (str): The configuration key to retrieve.
        default (bool): Default value if the key is not found.

    Returns:
        bool: The resolved boolean configuration value.
    """
    val = get_config_value(key, str(default)).strip().lower()
    return val in {"1", "true", "yes", "on"}


@lru_cache
def get_dry_run_mode() -> bool:
    """
    Return whether the application is running in dry-run mode.

    Returns:
        bool: True if DRY_RUN is set to a truthy value.
    """
    return get_config_bool("DRY_RUN", False)


@lru_cache
def get_environment() -> str:
    """
    Return the runtime environment.

    Returns:
        str: The environment name, e.g., 'dev', 'staging', or 'prod'.
    """
    return get_config_value("ENVIRONMENT", "dev")


@lru_cache
def get_poller_name() -> str:
    """
    Return the unique name identifying this poller.

    Returns:
        str: Poller name used in logs and queue bindings.
    """
    return get_config_value("POLLER_NAME", "replace_me_poller_name")


@lru_cache
def get_polling_interval() -> int:
    """
    Return the interval in seconds between polling operations.

    Returns:
        int: Number of seconds between poll cycles.
    """
    return int(get_config_value("POLLING_INTERVAL", "60"))


@lru_cache
def get_batch_size() -> int:
    """
    Return the number of items to process in a single batch.

    Returns:
        int: Batch size for processing messages.
    """
    return int(get_config_value("BATCH_SIZE", "10"))


@lru_cache
def get_rate_limit() -> int:
    """
    Return the rate limit in requests per second.

    Returns:
        int: Requests per second (0 = unlimited).
    """
    return int(get_config_value("RATE_LIMIT", "0"))


@lru_cache
def get_output_mode() -> OutputMode:
    """
    Return the configured output mode (e.g., 'queue', 'db', 's3').

    Returns:
        OutputMode: Enum representing the output mode.

    Raises:
        ValueError: If the mode is not a valid OutputMode.
    """
    raw_value = get_config_value("OUTPUT_MODE", "queue").lower()
    try:
        return OutputMode(raw_value)
    except ValueError:
        raise ValueError(
            f"❌ Invalid OUTPUT_MODE: '{raw_value}'. Must be one of: {[m.value for m in OutputMode]}"
        )


@lru_cache
def get_output_modes() -> list[str]:
    """
    Return a list of enabled output modes (e.g., ['queue', 'log']).

    Returns:
        list[str]: Lowercased output modes from comma-separated string.
    """
    raw = get_config_value("OUTPUT_MODES", get_output_mode().value)
    return [m.strip().lower() for m in raw.split(",") if m.strip()]


@lru_cache
def get_queue_type() -> str:
    """
    Return the type of message queue in use.

    Returns:
        str: Queue type (e.g., 'rabbitmq', 'sqs').
    """
    return get_config_value("QUEUE_TYPE", "rabbitmq")


@lru_cache
def get_rabbitmq_host() -> str:
    """
    Return the hostname of the RabbitMQ broker.

    Returns:
        str: Hostname of the RabbitMQ server.
    """
    return get_config_value("RABBITMQ_HOST", "localhost")


@lru_cache
def get_rabbitmq_port() -> int:
    """
    Return the port number for RabbitMQ.

    Returns:
        int: Port used to connect to RabbitMQ.
    """
    return int(get_config_value("RABBITMQ_PORT", "5672"))


@lru_cache
def get_rabbitmq_vhost() -> str:
    """
    Return the RabbitMQ virtual host.

    Returns:
        str: Virtual host name.

    Raises:
        ValueError: If the virtual host is not configured.
    """
    vhost = get_config_value("RABBITMQ_VHOST")
    if not vhost:
        raise ValueError("❌ Missing required config: RABBITMQ_VHOST must be set.")
    return vhost


@lru_cache
def get_rabbitmq_user() -> str:
    """
    Return the RabbitMQ username.

    Returns:
        str: Username for authenticating to RabbitMQ.
    """
    return get_config_value("RABBITMQ_USER", "")


@lru_cache
def get_rabbitmq_password() -> str:
    """
    Return the RabbitMQ password.

    Returns:
        str: Password for authenticating to RabbitMQ.
    """
    return get_config_value("RABBITMQ_PASS", "")


@lru_cache
def get_rabbitmq_exchange() -> str:
    """
    Return the RabbitMQ exchange name.

    Returns:
        str: Exchange name to publish/subscribe to.
    """
    return get_config_value("RABBITMQ_EXCHANGE", "stock_data_exchange")


@lru_cache
def get_rabbitmq_routing_key() -> str:
    """
    Return the RabbitMQ routing key.

    Returns:
        str: Routing key for message publishing.
    """
    return get_config_value("RABBITMQ_ROUTING_KEY", "stock_data")


@lru_cache
def get_rabbitmq_queue() -> str:
    """
    Return the name of the RabbitMQ queue to consume from.

    Returns:
        str: Queue name.
    """
    return get_config_value("RABBITMQ_QUEUE", "default_queue")


@lru_cache
def get_dlq_name() -> str:
    """
    Return the name of the Dead Letter Queue (DLQ) for failed messages.

    Returns:
        str: DLQ queue name.
    """
    return get_config_value("DLQ_NAME", "default_dlq")


@lru_cache
def get_sqs_queue_url() -> str:
    """
    Return the AWS SQS queue URL.

    Returns:
        str: Full SQS queue URL.
    """
    return get_config_value("SQS_QUEUE_URL", "")


@lru_cache
def get_sqs_region() -> str:
    """
    Return the AWS region for SQS operations.

    Returns:
        str: AWS region name.
    """
    return get_config_value("SQS_REGION", "us-east-1")


@lru_cache
def get_log_level() -> str:
    """
    Return the application log level.

    Returns:
        str: Logging level (e.g., 'INFO', 'DEBUG').
    """
    return get_config_value("LOG_LEVEL", "INFO")


@lru_cache
def get_poller_type() -> str:
    """
    Return the type/category of this poller.

    Returns:
        str: Label identifying the poller type (e.g., 'stock', 'sentiment').
    """
    return get_config_value("POLLER_TYPE", "stock")


@lru_cache
def get_retry_delay() -> int:
    """
    Return the number of seconds to wait before retrying failed operations.

    Returns:
        int: Retry delay in seconds.
    """
    return int(get_config_value("RETRY_DELAY", "5"))


@lru_cache
def get_symbols() -> List[str]:
    """
    Return a list of stock symbols to process.

    Returns:
        List[str]: Symbols parsed from comma-separated config.
    """
    symbols = get_config_value("SYMBOLS", "")
    return [s.strip() for s in symbols.split(",") if s.strip()]


@lru_cache
def get_newsapi_key() -> str:
    """
    Return the NewsAPI key used for fetching news articles.

    Returns:
        str: NewsAPI key.
    """
    return get_config_value("NEWSAPI_KEY")


@lru_cache
def get_newsapi_rate_limit() -> Tuple[int, int]:
    """
    Return the NewsAPI rate limit settings.

    Returns:
        Tuple[int, int]: (requests per second, burst capacity).
    """
    return (
        int(get_config_value("NEWSAPI_RATE", "5")),
        int(get_config_value("NEWSAPI_CAPACITY", "10")),
    )


@lru_cache
def get_newsapi_timeout() -> int:
    """
    Return the timeout in seconds for NewsAPI requests.

    Returns:
        int: Timeout duration.
    """
    return int(get_config_value("NEWSAPI_TIMEOUT", "10"))


@lru_cache
def get_youtube_api_key() -> str:
    """
    Return the YouTube Data API key.

    Returns:
        str: YouTube API key.
    """
    return get_config_value("YOUTUBE_API_KEY")


@lru_cache
def get_reddit_client_id() -> str:
    """
    Return the Reddit client ID for OAuth.

    Returns:
        str: Reddit client ID.
    """
    return get_config_value("REDDIT_CLIENT_ID")


@lru_cache
def get_reddit_client_secret() -> str:
    """
    Return the Reddit client secret for OAuth.

    Returns:
        str: Reddit client secret.
    """
    return get_config_value("REDDIT_CLIENT_SECRET")


@lru_cache
def get_alpha_vantage_api_key() -> str:
    """
    Return the Alpha Vantage API key.

    Returns:
        str: Alpha Vantage API key.
    """
    return get_secret_or_env("ALPHA_VANTAGE_API_KEY")


@lru_cache
def get_alpha_vantage_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Alpha Vantage.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("ALPHA_VANTAGE_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_finnhub_api_key() -> str:
    """
    Return the Finnhub API key.

    Returns:
        str: Finnhub API key.
    """
    return get_secret_or_env("FINNHUB_API_KEY")


@lru_cache
def get_finnhub_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Finnhub.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("FINNHUB_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_polygon_api_key() -> str:
    """
    Return the Polygon.io API key.

    Returns:
        str: Polygon API key.
    """
    return get_secret_or_env("POLYGON_API_KEY")


@lru_cache
def get_polygon_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Polygon.io.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("POLYGON_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_iex_api_key() -> str:
    """
    Return the IEX Cloud API key.

    Returns:
        str: IEX Cloud API key.
    """
    return get_secret_or_env("IEX_API_KEY")


@lru_cache
def get_iex_fill_rate_limit() -> int:
    """
    Return the fill rate limit for IEX.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("IEX_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_intrinio_key() -> str:
    """
    Return the Intrinio API key.

    Returns:
        str: Intrinio API key.
    """
    return get_secret_or_env("INTRINIO_API_KEY")


@lru_cache
def get_intrinio_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Intrinio.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("INTRINIO_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_quandl_api_key() -> str:
    """
    Return the Quandl API key.

    Returns:
        str: Quandl API key.
    """
    return get_secret_or_env("QUANDL_API_KEY")


@lru_cache
def get_quandl_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Quandl.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("QUANDL_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_yfinance_fill_rate_limit() -> int:
    """
    Return the fill rate limit for yFinance.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("YFINANCE_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_finnazon_key() -> str:
    """
    Return the Finnazon API key.

    Returns:
        str: Finnazon API key.
    """
    return get_secret_or_env("FINNAZON_API_KEY")


@lru_cache
def get_finnazon_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Finnazon.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("FINNAZON_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_rapidapi_key() -> str:
    """
    Return the RapidAPI key for Yahoo Finance.

    Returns:
        str: RapidAPI key.
    """
    return get_secret_or_env("RAPIDAPI_KEY")


@lru_cache
def get_rapidapi_host() -> str:
    """
    Return the RapidAPI host for Yahoo Finance.

    Returns:
        str: RapidAPI host string.
    """
    return get_secret_or_env("RAPIDAPI_HOST", default="yahoo-finance15.p.rapidapi.com")


@lru_cache
def get_benzinga_api_key() -> str:
    """
    Return the Benzinga API key from secrets or environment.

    Returns:
        str: Benzinga API key.
    """
    return get_secret_or_env("BENZINGA_API_KEY")


@lru_cache
def get_benzinga_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Benzinga polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("BENZINGA_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_barchart_api_key() -> str:
    """
    Return the Barchart API key from secrets or environment.

    Returns:
        str: Barchart API key.
    """
    return get_secret_or_env("BARCHART_API_KEY")


@lru_cache
def get_barchart_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Barchart polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("BARCHART_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_twelvedata_api_key() -> str:
    """
    Return the Twelve Data API key from secrets or environment.

    Returns:
        str: Twelve Data API key.
    """
    return get_secret_or_env("TWELVEDATA_API_KEY")


@lru_cache
def get_twelvedata_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Twelve Data polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("TWELVEDATA_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_coinmarketcap_api_key() -> str:
    """
    Return the CoinMarketCap API key from secrets or environment.

    Returns:
        str: CoinMarketCap API key.
    """
    return get_secret_or_env("COINMARKETCAP_API_KEY")


@lru_cache
def get_coinmarketcap_fill_rate_limit() -> int:
    """
    Return the fill rate limit for CoinMarketCap polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("COINMARKETCAP_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_coinapi_key() -> str:
    """
    Return the CoinAPI key from secrets or environment.

    Returns:
        str: CoinAPI key.
    """
    return get_secret_or_env("COINAPI_KEY")


@lru_cache
def get_coinapi_fill_rate_limit() -> int:
    """
    Return the fill rate limit for CoinAPI polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("COINAPI_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_morningstar_api_key() -> str:
    """
    Return the Morningstar API key from secrets or environment.

    Returns:
        str: Morningstar API key.
    """
    return get_secret_or_env("MORNINGSTAR_API_KEY")


@lru_cache
def get_morningstar_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Morningstar polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("MORNINGSTAR_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_seekingalpha_api_key() -> str:
    """
    Return the SeekingAlpha API key from secrets or environment.

    Returns:
        str: SeekingAlpha API key.
    """
    return get_secret_or_env("SEEKINGALPHA_API_KEY")


@lru_cache
def get_seekingalpha_fill_rate_limit() -> int:
    """
    Return the fill rate limit for SeekingAlpha polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("SEEKINGALPHA_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_sentimentinvestor_api_key() -> str:
    """
    Return the Sentiment Investor API key from secrets or environment.

    Returns:
        str: Sentiment Investor API key.
    """
    return get_secret_or_env("SENTIMENTINVESTOR_API_KEY")


@lru_cache
def get_sentimentinvestor_fill_rate_limit() -> int:
    """
    Return the fill rate limit for Sentiment Investor polling.

    Returns:
        int: Requests per minute.
    """
    return int(get_secret_or_env("SENTIMENTINVESTOR_FILL_RATE_LIMIT", default="60"))


@lru_cache
def get_structured_logging() -> bool:
    """
    Return whether structured (JSON) logging is enabled.

    Returns:
        bool: True if STRUCTURED_LOGGING is enabled.
    """
    return get_config_bool("STRUCTURED_LOGGING", False)


@lru_cache
def get_redact_sensitive_logs() -> bool:
    """
    Return whether sensitive fields should be redacted from logs.

    Returns:
        bool: True if redaction is enabled.
    """
    return get_config_bool("REDACT_SENSITIVE_LOGS", True)


@lru_cache
def get_debug_mode() -> bool:
    """
    Return whether the application is in debug mode.

    Returns:
        bool: True if debug mode is enabled.
    """
    return get_config_bool("DEBUG", False)


@lru_cache
def get_healthcheck_enabled() -> bool:
    """
    Return whether healthchecks are enabled for this service.

    Returns:
        bool: True if healthchecks should be run.
    """
    return get_config_bool("HEALTHCHECK_ENABLED", True)


@lru_cache
def get_service_name() -> str:
    """
    Return the human-readable name of this service.

    Returns:
        str: Service name, defaults to the poller name.
    """
    return get_config_value("SERVICE_NAME", get_poller_name())


@lru_cache
def get_crypto_symbols() -> List[str]:
    """
    Return a list of cryptocurrency symbols to poll (e.g., BTC, ETH).

    Returns:
        List[str]: A list of uppercased symbol strings.
    """
    symbols = get_config_value("CRYPTO_SYMBOLS", "")
    return [s.strip().upper() for s in symbols.split(",") if s.strip()]


@lru_cache
def get_crypto_exchange() -> str:
    """
    Return the exchange name used for crypto polling.

    Returns:
        str: Exchange name (e.g., 'binance').
    """
    return get_config_value("CRYPTO_EXCHANGE", "binance")


@lru_cache
def get_crypto_network() -> str:
    """
    Return the blockchain network used for data collection.

    Returns:
        str: Network name (e.g., 'ethereum').
    """
    return get_config_value("CRYPTO_NETWORK", "ethereum")


@lru_cache
def get_crypto_data_source() -> str:
    """
    Return the data provider name used for crypto polling.

    Returns:
        str: Provider name (e.g., 'coinmarketcap').
    """
    return get_config_value("CRYPTO_DATA_SOURCE", "coinmarketcap")


@lru_cache
def get_crypto_queue_name() -> str:
    """
    Return the queue name to route crypto messages.

    Returns:
        str: Queue name.
    """
    return get_config_value("CRYPTO_QUEUE_NAME", "crypto_data_queue")


@lru_cache
def get_crypto_polling_interval() -> int:
    """
    Return polling interval for crypto services.

    Returns:
        int: Polling interval in seconds.
    """
    return int(get_config_value("CRYPTO_POLLING_INTERVAL", str(get_polling_interval())))


@lru_cache
def get_crypto_retry_delay() -> int:
    """
    Return retry delay after a failed crypto API call.

    Returns:
        int: Delay in seconds.
    """
    return int(get_config_value("CRYPTO_RETRY_DELAY", "10"))


@lru_cache
def get_crypto_rate_limit() -> int:
    """
    Return the rate limit in requests per second for crypto APIs.

    Returns:
        int: Requests per second.
    """
    return int(get_config_value("CRYPTO_RATE_LIMIT", "5"))


@lru_cache
def get_candle_granularity() -> str:
    """
    Return candlestick data granularity.

    Returns:
        str: Interval string (e.g., '1m', '5m').
    """
    return get_config_value("CANDLE_GRANULARITY", "1m")


@lru_cache
def get_lookback_period_minutes() -> int:
    """
    Return lookback window for historical data in minutes.

    Returns:
        int: Number of minutes.
    """
    return int(get_config_value("LOOKBACK_PERIOD_MINUTES", "60"))


@lru_cache
def get_websocket_enabled() -> bool:
    """
    Return whether WebSocket streaming is enabled.

    Returns:
        bool: True if enabled, else False.
    """
    return get_config_bool("WEBSOCKET_ENABLED", False)


@lru_cache
def get_websocket_url() -> str:
    """
    Return the WebSocket endpoint URL.

    Returns:
        str: URL string.
    """
    return get_config_value("WEBSOCKET_URL", "")


@lru_cache
def get_websocket_auth_token() -> str:
    """
    Return WebSocket authentication token if required.

    Returns:
        str: Auth token or empty string.
    """
    return get_secret_or_env("WEBSOCKET_AUTH_TOKEN", "")


@lru_cache
def get_coingecko_fill_rate_limit() -> int:
    """
    Return CoinGecko fill rate limit (no API key).

    Returns:
        int: Requests per second.
    """
    return int(get_config_value("COINGECKO_FILL_RATE_LIMIT", "20"))


@lru_cache
def get_cryptocompare_api_key() -> str:
    """
    Return CryptoCompare API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("CRYPTOCOMPARE_API_KEY")


@lru_cache
def get_cryptocompare_fill_rate_limit() -> int:
    """
    Return CryptoCompare fill rate limit.

    Returns:
        int: Requests per second.
    """
    return int(get_secret_or_env("CRYPTOCOMPARE_FILL_RATE_LIMIT", "60"))


@lru_cache
def get_glassnode_api_key() -> str:
    """
    Return Glassnode API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("GLASSNODE_API_KEY")


@lru_cache
def get_messari_api_key() -> str:
    """
    Return Messari API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("MESSARI_API_KEY")


@lru_cache
def get_nomics_api_key() -> str:
    """
    Return Nomics API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("NOMICS_API_KEY")


@lru_cache
def get_kaiko_api_key() -> str:
    """
    Return Kaiko API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("KAIKO_API_KEY")


@lru_cache
def get_intotheblock_api_key() -> str:
    """
    Return IntoTheBlock API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("INTOTHEBLOCK_API_KEY")


@lru_cache
def get_binance_api_key() -> str:
    """
    Return Binance API key for authenticated endpoints.

    Returns:
        str: API key.
    """
    return get_secret_or_env("BINANCE_API_KEY")


@lru_cache
def get_binance_api_secret() -> str:
    """
    Return Binance API secret.

    Returns:
        str: API secret.
    """
    return get_secret_or_env("BINANCE_API_SECRET")


@lru_cache
def get_kraken_api_key() -> str:
    """
    Return Kraken API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("KRAKEN_API_KEY")


@lru_cache
def get_kraken_api_secret() -> str:
    """
    Return Kraken API secret.

    Returns:
        str: API secret.
    """
    return get_secret_or_env("KRAKEN_API_SECRET")


@lru_cache
def get_huobi_api_key() -> str:
    """
    Return Huobi API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("HUOBI_API_KEY")


@lru_cache
def get_huobi_api_secret() -> str:
    """
    Return Huobi API secret.

    Returns:
        str: API secret.
    """
    return get_secret_or_env("HUOBI_API_SECRET")


@lru_cache
def get_okx_api_key() -> str:
    """
    Return OKX API key.

    Returns:
        str: API key.
    """
    return get_secret_or_env("OKX_API_KEY")


@lru_cache
def get_okx_api_secret() -> str:
    """
    Return OKX API secret.

    Returns:
        str: API secret.
    """
    return get_secret_or_env("OKX_API_SECRET")


@lru_cache
def get_okx_passphrase() -> str:
    """
    Return OKX API passphrase.

    Returns:
        str: API passphrase.
    """
    return get_secret_or_env("OKX_PASSPHRASE")
